from typing import Any, Dict, FrozenSet


CHECKLIST_RESPONSE_YES = "YES"

CHECKLIST_RESPONSE_NO = "NO"

CHECKLIST_RESPONSE_NOT_APPLICABLE = (
    "NOT_APPLICABLE"
)


CHECKLIST_RESPONSE_STATUSES: FrozenSet[str] = frozenset(
    {
        CHECKLIST_RESPONSE_YES,
        CHECKLIST_RESPONSE_NO,
        CHECKLIST_RESPONSE_NOT_APPLICABLE,
    }
)


CHECKLIST_REASON_REQUIRED_STATUSES: FrozenSet[str] = (
    frozenset(
        {
            CHECKLIST_RESPONSE_NO,
            CHECKLIST_RESPONSE_NOT_APPLICABLE,
        }
    )
)


CHECKLIST_RESPONSE_LABELS: Dict[str, str] = {
    CHECKLIST_RESPONSE_YES: "Yes",
    CHECKLIST_RESPONSE_NO: "No",
    CHECKLIST_RESPONSE_NOT_APPLICABLE: (
        "Not applicable"
    ),
}


MAX_CHECKLIST_REASON_LENGTH = 2000


def normalize_checklist_response(
    value: Any,
) -> str:
    """
    Return the canonical checklist-response value used by the
    database and validation services.
    """

    return str(
        value or ""
    ).strip().upper()


def is_supported_checklist_response(
    response_status: Any,
) -> bool:
    """
    Return whether the supplied value is an approved checklist
    response.
    """

    normalized_status = normalize_checklist_response(
        response_status
    )

    return (
        normalized_status
        in CHECKLIST_RESPONSE_STATUSES
    )


def checklist_response_requires_reason(
    response_status: Any,
) -> bool:
    """
    Return whether an explanation is mandatory for this response.
    """

    normalized_status = normalize_checklist_response(
        response_status
    )

    return (
        normalized_status
        in CHECKLIST_REASON_REQUIRED_STATUSES
    )


def get_checklist_response_label(
    response_status: Any,
) -> str:
    """
    Return the user-facing label for a stored checklist response.
    """

    normalized_status = normalize_checklist_response(
        response_status
    )

    if not normalized_status:
        return "Not recorded"

    return CHECKLIST_RESPONSE_LABELS.get(
        normalized_status,
        normalized_status.replace(
            "_",
            " ",
        ).title(),
    )