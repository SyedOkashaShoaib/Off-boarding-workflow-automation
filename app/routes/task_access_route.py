from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    url_for,
)
from sqlalchemy.exc import SQLAlchemyError

from app.extension import db
from app.forms.auth_forms import (
    TaskAccessContinueForm,
)
from app.services.task_access_service import (
    activate_pending_task_access,
    clear_task_access_session,
    find_redeemable_grant,
    set_pending_task_access,
)


task_access_bp = Blueprint(
    "task_access",
    __name__,
    url_prefix="/task-access",
)


def render_unavailable():
    """
    Return a neutral response without revealing task existence.
    """

    clear_task_access_session()

    return (
        render_template(
            "task_access/unavailable.html"
        ),
        404,
    )
def redirect_to_grant_task(
    grant,
):
    """
    Redirect an authorized grant to its correct workflow interface.
    """

    task = grant.workflow_task

    if task.phase.is_final_approval:
        endpoint = (
            "workflow.admin_approval"
        )
    else:
        endpoint = (
            "workflow.view_task"
        )

    return redirect(
        url_for(
            endpoint,
            task_id=task.id,
        )
    )

@task_access_bp.after_request
def secure_task_access_response(response):
    """
    Prevent token pages and employee information from being cached
    or exposed through referrer headers.
    """

    response.headers[
        "Cache-Control"
    ] = "no-store, private"

    response.headers[
        "Referrer-Policy"
    ] = "no-referrer"

    return response


@task_access_bp.get("/<string:raw_token>")
def access_link(raw_token):
    """
    Validate an emailed access token and display a continuation page.

    This GET does not mark the task as opened.
    """

    grant = find_redeemable_grant(
        raw_token
    )

    if grant is None:
        return render_unavailable()

    set_pending_task_access(grant)

    form = TaskAccessContinueForm()

    return render_template(
        "task_access/continue.html",
        task=grant.workflow_task,
        form=form,
    )


@task_access_bp.post("/continue")
def continue_to_task():
    """
    Establish the limited task session after explicit confirmation
    and redirect to the correct workflow interface.
    """

    form = TaskAccessContinueForm()

    if not form.validate_on_submit():
        return render_unavailable()

    grant = activate_pending_task_access()

    if grant is None:
        return render_unavailable()

    task = grant.workflow_task

    if task is None:
        clear_task_access_session()

        current_app.logger.error(
            (
                "Task-access grant %s does not reference "
                "a valid workflow task."
            ),
            grant.id,
        )

        return render_unavailable()

    try:
        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        clear_task_access_session()

        current_app.logger.exception(
            "Could not activate task-access grant %s.",
            grant.id,
        )

        return (
            render_template(
                "task_access/unavailable.html"
            ),
            503,
        )

    if task.phase.is_final_approval:
        destination_endpoint = (
            "workflow.admin_approval"
        )
    else:
        destination_endpoint = (
            "workflow.view_task"
        )

    return redirect(
        url_for(
            destination_endpoint,
            task_id=task.id,
        )
    )