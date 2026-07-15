"""
Query and presentation-data service for the NOC case register.

This module contains no Flask request or template logic. Routes pass
request arguments into this service and receive validated, paginated
data suitable for presentation.
"""

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from math import ceil
from typing import (
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
)

from sqlalchemy import (
    and_,
    case as sql_case,
    func,
    or_,
)
from sqlalchemy.orm import aliased

from app.extension import db
from app.models import (
    Department,
    OffboardingCase,
    WorkflowPhase,
    WorkflowTask,
    utc_now,
)


# ============================================================
# Case and task states
# ============================================================

ACTIVE_CASE_STATUSES = (
    "CREATED",
    "IN_PROGRESS",
)

CLOSED_CASE_STATUS = "CLOSED"

OPEN_TASK_STATUSES = (
    "PENDING",
    "IN_PROGRESS",
)


# ============================================================
# Register filter values
# ============================================================

CASE_FILTER_ACTIVE = "active"
CASE_FILTER_CLOSED = "closed"
CASE_FILTER_ALL = "all"

ALLOWED_CASE_FILTERS = {
    CASE_FILTER_ACTIVE,
    CASE_FILTER_CLOSED,
    CASE_FILTER_ALL,
}


DUE_FILTER_ALL = "all"
DUE_FILTER_ON_TIME = "on_time"
DUE_FILTER_DUE_SOON = "due_soon"
DUE_FILTER_OVERDUE = "overdue"

ALLOWED_DUE_FILTERS = {
    DUE_FILTER_ALL,
    DUE_FILTER_ON_TIME,
    DUE_FILTER_DUE_SOON,
    DUE_FILTER_OVERDUE,
}


DUE_STATE_NOT_APPLICABLE = "not_applicable"


ATTENTION_NONE = "none"
ATTENTION_DUE_SOON = "due_soon"
ATTENTION_OVERDUE = "overdue"
ATTENTION_AWAITING_APPROVAL = "awaiting_approval"
ATTENTION_WORKFLOW_ISSUE = "workflow_issue"


DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 25

ALLOWED_PER_PAGE_VALUES = {
    25,
    50,
    100,
}

MAX_SEARCH_LENGTH = 100
DUE_SOON_HOURS = 48


# ============================================================
# Public data contracts
# ============================================================

@dataclass(frozen=True)
class CaseRegisterFilters:
    """
    Validated filters used by the case-register query.

    phase_slug is None when all phases should be included.
    """

    search: str = ""
    case_status: str = CASE_FILTER_ACTIVE
    phase_slug: Optional[str] = None
    due_state: str = DUE_FILTER_ALL
    page: int = DEFAULT_PAGE
    per_page: int = DEFAULT_PER_PAGE


@dataclass(frozen=True)
class PhaseFilterOption:
    """One workflow phase available in the phase filter."""

    slug: str
    name: str
    department_name: str
    phase_order: int
    is_final_approval: bool


@dataclass(frozen=True)
class CaseRegisterItem:
    """
    One case-register table row.

    The template should consume this object instead of performing
    additional relationship queries for every displayed case.
    """

    case_id: int
    case_number: str

    employee_name: str
    employee_id: str
    employee_department: str
    designation: str

    case_status: str

    current_phase_id: Optional[int]
    current_phase_name: Optional[str]
    current_phase_slug: Optional[str]
    current_department_name: Optional[str]
    current_phase_is_final_approval: bool

    current_task_id: Optional[int]
    current_task_status: Optional[str]
    current_task_due_at: Optional[datetime]

    due_state: str
    attention_code: str

    last_working_day: object
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]


@dataclass(frozen=True)
class CaseRegisterPage:
    """A normalized page of case-register records."""

    items: Tuple[CaseRegisterItem, ...]

    page: int
    per_page: int
    total: int
    pages: int

    has_previous: bool
    has_next: bool
    previous_page: Optional[int]
    next_page: Optional[int]


@dataclass(frozen=True)
class CaseRegisterCounts:
    """
    Global case-register quick-view counts.

    These counts are intentionally independent of the currently
    selected search and filters.
    """

    all_cases: int
    active_cases: int
    overdue_cases: int
    awaiting_approval_cases: int
    closed_cases: int


@dataclass(frozen=True)
class CaseRegisterData:
    """
    Complete service response required by the future Cases page.
    """

    filters: CaseRegisterFilters
    phase_options: Tuple[PhaseFilterOption, ...]
    page: CaseRegisterPage
    counts: CaseRegisterCounts


# ============================================================
# Filter parsing
# ============================================================

def _clean_text(
    value: object,
    *,
    maximum_length: int,
) -> str:
    """
    Convert an arbitrary query-parameter value into bounded text.
    """

    if value is None:
        return ""

    return str(value).strip()[:maximum_length]


def _parse_positive_integer(
    value: object,
    *,
    default: int,
) -> int:
    """
    Return a positive integer or the supplied safe default.
    """

    try:
        parsed_value = int(str(value))
    except (TypeError, ValueError):
        return default

    if parsed_value < 1:
        return default

    return parsed_value


def parse_case_register_filters(
    arguments: Mapping[str, object],
    valid_phase_slugs: Sequence[str],
) -> CaseRegisterFilters:
    """
    Parse and validate case-register query parameters.

    Unknown or malformed values fall back to safe defaults.
    Arbitrary URL values are never used to select query behaviour.
    """

    valid_phase_slug_set: Set[str] = {
        slug.strip().lower()
        for slug in valid_phase_slugs
        if slug and slug.strip()
    }

    search = _clean_text(
        arguments.get("q"),
        maximum_length=MAX_SEARCH_LENGTH,
    )

    requested_case_status = _clean_text(
        arguments.get("status"),
        maximum_length=20,
    ).lower()

    if requested_case_status not in ALLOWED_CASE_FILTERS:
        requested_case_status = CASE_FILTER_ACTIVE

    requested_due_state = _clean_text(
        arguments.get("due_state"),
        maximum_length=20,
    ).lower()

    if requested_due_state not in ALLOWED_DUE_FILTERS:
        requested_due_state = DUE_FILTER_ALL

    requested_phase = _clean_text(
        arguments.get("phase"),
        maximum_length=100,
    ).lower()

    phase_slug = None

    if (
        requested_phase
        and requested_phase != "all"
        and requested_phase in valid_phase_slug_set
    ):
        phase_slug = requested_phase

    page = _parse_positive_integer(
        arguments.get("page"),
        default=DEFAULT_PAGE,
    )

    requested_per_page = _parse_positive_integer(
        arguments.get("per_page"),
        default=DEFAULT_PER_PAGE,
    )

    if requested_per_page not in ALLOWED_PER_PAGE_VALUES:
        requested_per_page = DEFAULT_PER_PAGE

    return CaseRegisterFilters(
        search=search,
        case_status=requested_case_status,
        phase_slug=phase_slug,
        due_state=requested_due_state,
        page=page,
        per_page=requested_per_page,
    )


# ============================================================
# Query helpers
# ============================================================

def get_phase_filter_options() -> Tuple[PhaseFilterOption, ...]:
    """
    Return active workflow phases in operational order.
    """

    rows = (
        db.session.query(
            WorkflowPhase,
            Department,
        )
        .join(
            Department,
            WorkflowPhase.department_id == Department.id,
        )
        .filter(
            WorkflowPhase.is_active.is_(True),
            Department.is_active.is_(True),
        )
        .order_by(
            WorkflowPhase.phase_order.asc(),
            WorkflowPhase.id.asc(),
        )
        .all()
    )

    return tuple(
        PhaseFilterOption(
            slug=phase.slug,
            name=phase.name,
            department_name=department.name,
            phase_order=phase.phase_order,
            is_final_approval=phase.is_final_approval,
        )
        for phase, department in rows
    )


def _escape_like_value(value: str) -> str:
    """
    Escape SQL LIKE wildcard characters in user-entered search text.

    Percent and underscore should be interpreted as literal user
    input rather than as wildcard instructions.
    """

    return (
        value
        .replace("\\", "\\\\")
        .replace("%", "\\%")
        .replace("_", "\\_")
    )


def _normalize_datetime(
    value: Optional[datetime],
) -> Optional[datetime]:
    """
    Return a timezone-aware UTC datetime.

    SQLite may return a naive datetime even when the model column was
    declared with timezone=True.
    """

    if value is None:
        return None

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


def _determine_due_state(
    *,
    case_status: str,
    task: Optional[WorkflowTask],
    current_time: datetime,
) -> str:
    """
    Determine the operational due state of the current task.
    """

    if case_status == CLOSED_CASE_STATUS:
        return DUE_STATE_NOT_APPLICABLE

    if task is None:
        return DUE_STATE_NOT_APPLICABLE

    if task.status not in OPEN_TASK_STATUSES:
        return DUE_STATE_NOT_APPLICABLE

    task_due_at = _normalize_datetime(task.due_at)

    if task_due_at is None:
        return DUE_STATE_NOT_APPLICABLE

    due_soon_cutoff = (
        current_time
        + timedelta(hours=DUE_SOON_HOURS)
    )

    if task_due_at <= current_time:
        return DUE_FILTER_OVERDUE

    if task_due_at <= due_soon_cutoff:
        return DUE_FILTER_DUE_SOON

    return DUE_FILTER_ON_TIME


def _determine_attention_code(
    *,
    offboarding_case: OffboardingCase,
    current_task: Optional[WorkflowTask],
    current_phase: Optional[WorkflowPhase],
    due_state: str,
) -> str:
    """
    Determine the highest-priority condition for the register row.
    """

    if offboarding_case.status == CLOSED_CASE_STATUS:
        return ATTENTION_NONE

    if current_phase is None or current_task is None:
        return ATTENTION_WORKFLOW_ISSUE

    if current_task.status not in OPEN_TASK_STATUSES:
        return ATTENTION_WORKFLOW_ISSUE

    if due_state == DUE_FILTER_OVERDUE:
        return ATTENTION_OVERDUE

    if due_state == DUE_FILTER_DUE_SOON:
        return ATTENTION_DUE_SOON

    if current_phase.is_final_approval:
        return ATTENTION_AWAITING_APPROVAL

    return ATTENTION_NONE


def _build_register_item(
    *,
    offboarding_case: OffboardingCase,
    current_task: Optional[WorkflowTask],
    current_phase: Optional[WorkflowPhase],
    current_department: Optional[Department],
    current_time: datetime,
) -> CaseRegisterItem:
    """
    Convert ORM query results into a stable presentation contract.
    """

    due_state = _determine_due_state(
        case_status=offboarding_case.status,
        task=current_task,
        current_time=current_time,
    )

    attention_code = _determine_attention_code(
        offboarding_case=offboarding_case,
        current_task=current_task,
        current_phase=current_phase,
        due_state=due_state,
    )

    return CaseRegisterItem(
        case_id=offboarding_case.id,
        case_number=offboarding_case.case_number,

        employee_name=offboarding_case.employee_name,
        employee_id=offboarding_case.employee_id,
        employee_department=offboarding_case.department,
        designation=offboarding_case.designation,

        case_status=offboarding_case.status,

        current_phase_id=(
            current_phase.id
            if current_phase is not None
            else None
        ),
        current_phase_name=(
            current_phase.name
            if current_phase is not None
            else None
        ),
        current_phase_slug=(
            current_phase.slug
            if current_phase is not None
            else None
        ),
        current_department_name=(
            current_department.name
            if current_department is not None
            else None
        ),
        current_phase_is_final_approval=(
            bool(current_phase.is_final_approval)
            if current_phase is not None
            else False
        ),

        current_task_id=(
            current_task.id
            if current_task is not None
            else None
        ),
        current_task_status=(
            current_task.status
            if current_task is not None
            else None
        ),
        current_task_due_at=(
            _normalize_datetime(current_task.due_at)
            if current_task is not None
            else None
        ),

        due_state=due_state,
        attention_code=attention_code,

        last_working_day=offboarding_case.last_working_day,
        created_at=_normalize_datetime(
            offboarding_case.created_at
        ),
        updated_at=_normalize_datetime(
            offboarding_case.updated_at
        ),
        closed_at=_normalize_datetime(
            offboarding_case.closed_at
        ),
    )


# ============================================================
# Register query
# ============================================================

def get_case_register_page(
    filters: CaseRegisterFilters,
    *,
    current_time: Optional[datetime] = None,
) -> CaseRegisterPage:
    """
    Return one filtered and paginated case-register page.

    The query joins only the case's current phase, department, and
    current task. Historical tasks, checklist responses, audit logs,
    and notification collections are not loaded for the register.
    """

    effective_time = _normalize_datetime(
        current_time or utc_now()
    )

    current_phase = aliased(
        WorkflowPhase,
        name="register_current_phase",
    )

    current_department = aliased(
        Department,
        name="register_current_department",
    )

    current_task = aliased(
        WorkflowTask,
        name="register_current_task",
    )

    query = (
        db.session.query(
            OffboardingCase,
            current_task,
            current_phase,
            current_department,
        )
        .outerjoin(
            current_phase,
            OffboardingCase.current_phase_id
            == current_phase.id,
        )
        .outerjoin(
            current_department,
            current_phase.department_id
            == current_department.id,
        )
        .outerjoin(
            current_task,
            and_(
                current_task.case_id
                == OffboardingCase.id,
                current_task.phase_id
                == OffboardingCase.current_phase_id,
            ),
        )
    )

    # --------------------------------------------------------
    # Case-status filter
    # --------------------------------------------------------

    if filters.case_status == CASE_FILTER_ACTIVE:
        query = query.filter(
            OffboardingCase.status.in_(
                ACTIVE_CASE_STATUSES
            )
        )

    elif filters.case_status == CASE_FILTER_CLOSED:
        query = query.filter(
            OffboardingCase.status
            == CLOSED_CASE_STATUS
        )

    # CASE_FILTER_ALL adds no case-status restriction.

    # --------------------------------------------------------
    # Phase filter
    # --------------------------------------------------------

    if filters.phase_slug is not None:
        query = query.filter(
            current_phase.slug == filters.phase_slug
        )

    # --------------------------------------------------------
    # Due-state filter
    # --------------------------------------------------------

    due_soon_cutoff = (
        effective_time
        + timedelta(hours=DUE_SOON_HOURS)
    )

    if filters.due_state == DUE_FILTER_OVERDUE:
        query = query.filter(
            current_task.status.in_(
                OPEN_TASK_STATUSES
            ),
            current_task.due_at <= effective_time,
        )

    elif filters.due_state == DUE_FILTER_DUE_SOON:
        query = query.filter(
            current_task.status.in_(
                OPEN_TASK_STATUSES
            ),
            current_task.due_at > effective_time,
            current_task.due_at <= due_soon_cutoff,
        )

    elif filters.due_state == DUE_FILTER_ON_TIME:
        query = query.filter(
            current_task.status.in_(
                OPEN_TASK_STATUSES
            ),
            current_task.due_at > due_soon_cutoff,
        )

    # --------------------------------------------------------
    # Search filter
    # --------------------------------------------------------

    if filters.search:
        escaped_search = _escape_like_value(
            filters.search
        )

        prefix_pattern = (
            f"{escaped_search}%"
        )

        contains_pattern = (
            f"%{escaped_search}%"
        )

        query = query.filter(
            or_(
                OffboardingCase.case_number.ilike(
                    prefix_pattern,
                    escape="\\",
                ),
                OffboardingCase.employee_id.ilike(
                    prefix_pattern,
                    escape="\\",
                ),
                OffboardingCase.employee_name.ilike(
                    contains_pattern,
                    escape="\\",
                ),
            )
        )

    # Stable secondary ordering by ID prevents records with identical
    # updated timestamps from moving between pages.
    query = query.order_by(
        OffboardingCase.updated_at.desc(),
        OffboardingCase.id.desc(),
    )

    pagination = query.paginate(
        page=filters.page,
        per_page=filters.per_page,
        error_out=False,
    )

    effective_filters = filters

    # Clamp out-of-range page numbers rather than returning a confusing
    # empty table when matching records exist.
    if pagination.total == 0:
        if filters.page != DEFAULT_PAGE:
            effective_filters = replace(
                filters,
                page=DEFAULT_PAGE,
            )

            pagination = query.paginate(
                page=DEFAULT_PAGE,
                per_page=filters.per_page,
                error_out=False,
            )

    elif (
        pagination.pages > 0
        and filters.page > pagination.pages
    ):
        effective_filters = replace(
            filters,
            page=pagination.pages,
        )

        pagination = query.paginate(
            page=pagination.pages,
            per_page=filters.per_page,
            error_out=False,
        )

    items: List[CaseRegisterItem] = []

    for (
        offboarding_case,
        task,
        phase,
        department,
    ) in pagination.items:
        items.append(
            _build_register_item(
                offboarding_case=offboarding_case,
                current_task=task,
                current_phase=phase,
                current_department=department,
                current_time=effective_time,
            )
        )

    total = int(pagination.total or 0)

    pages = (
        int(ceil(total / effective_filters.per_page))
        if total > 0
        else 0
    )

    has_previous = (
        total > 0
        and effective_filters.page > 1
    )

    has_next = (
        total > 0
        and effective_filters.page < pages
    )

    return CaseRegisterPage(
        items=tuple(items),

        page=effective_filters.page,
        per_page=effective_filters.per_page,
        total=total,
        pages=pages,

        has_previous=has_previous,
        has_next=has_next,

        previous_page=(
            effective_filters.page - 1
            if has_previous
            else None
        ),

        next_page=(
            effective_filters.page + 1
            if has_next
            else None
        ),
    )


# ============================================================
# Quick-view counts
# ============================================================

def get_case_register_counts(
    *,
    current_time: Optional[datetime] = None,
) -> CaseRegisterCounts:
    """
    Return global counts used by case-register quick filters.

    This uses one aggregate query rather than loading cases into
    Python or performing one query for each counter.
    """

    effective_time = _normalize_datetime(
        current_time or utc_now()
    )

    current_phase = aliased(
        WorkflowPhase,
        name="count_current_phase",
    )

    current_task = aliased(
        WorkflowTask,
        name="count_current_task",
    )

    is_active_case = (
        OffboardingCase.status.in_(
            ACTIVE_CASE_STATUSES
        )
    )

    is_overdue_case = and_(
        is_active_case,
        current_task.status.in_(
            OPEN_TASK_STATUSES
        ),
        current_task.due_at <= effective_time,
    )

    is_awaiting_approval = and_(
        is_active_case,
        current_phase.is_final_approval.is_(True),
    )

    result = (
        db.session.query(
            func.count(
                OffboardingCase.id
            ).label("all_cases"),

            func.coalesce(
                func.sum(
                    sql_case(
                        (
                            is_active_case,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("active_cases"),

            func.coalesce(
                func.sum(
                    sql_case(
                        (
                            is_overdue_case,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("overdue_cases"),

            func.coalesce(
                func.sum(
                    sql_case(
                        (
                            is_awaiting_approval,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label(
                "awaiting_approval_cases"
            ),

            func.coalesce(
                func.sum(
                    sql_case(
                        (
                            OffboardingCase.status
                            == CLOSED_CASE_STATUS,
                            1,
                        ),
                        else_=0,
                    )
                ),
                0,
            ).label("closed_cases"),
        )
        .outerjoin(
            current_phase,
            OffboardingCase.current_phase_id
            == current_phase.id,
        )
        .outerjoin(
            current_task,
            and_(
                current_task.case_id
                == OffboardingCase.id,
                current_task.phase_id
                == OffboardingCase.current_phase_id,
            ),
        )
        .one()
    )

    return CaseRegisterCounts(
        all_cases=int(result.all_cases or 0),
        active_cases=int(result.active_cases or 0),
        overdue_cases=int(result.overdue_cases or 0),
        awaiting_approval_cases=int(
            result.awaiting_approval_cases or 0
        ),
        closed_cases=int(result.closed_cases or 0),
    )


# ============================================================
# Route-facing service
# ============================================================

def get_case_register_data(
    arguments: Mapping[str, object],
) -> CaseRegisterData:
    """
    Return the complete case-register data contract.

    This is the primary function the future GET /cases/ route
    should call.
    """

    phase_options = get_phase_filter_options()

    filters = parse_case_register_filters(
        arguments=arguments,
        valid_phase_slugs=[
            option.slug
            for option in phase_options
        ],
    )

    page = get_case_register_page(
        filters=filters,
    )

    # The page service may clamp an out-of-range page. Reflect that
    # effective page in the public filter contract.
    if page.page != filters.page:
        filters = replace(
            filters,
            page=page.page,
        )

    counts = get_case_register_counts()

    return CaseRegisterData(
        filters=filters,
        phase_options=phase_options,
        page=page,
        counts=counts,
    )