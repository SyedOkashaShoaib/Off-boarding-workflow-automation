"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("[data-checklist-form]");

    if (!form) {
        return;
    }

    const checklistItems = form.querySelectorAll(
        "[data-checklist-item]"
    );

    checklistItems.forEach((item) => {
        const yesInput = item.querySelector(
            'input[type="radio"][value="YES"]'
        );

        const notApplicableInput = item.querySelector(
            'input[type="radio"][value="NOT_APPLICABLE"]'
        );

        const reasonContainer = item.querySelector(
            "[data-reason-container]"
        );

        const reasonInput = item.querySelector(
            "[data-reason-input]"
        );

        if (
            !yesInput
            || !notApplicableInput
            || !reasonContainer
            || !reasonInput
        ) {
            return;
        }

        const updateReasonState = () => {
            const isNotApplicable =
                notApplicableInput.checked;

            reasonContainer.classList.toggle(
                "is-collapsed",
                !isNotApplicable
            );

            reasonInput.disabled = !isNotApplicable;
            reasonInput.required = isNotApplicable;

            reasonInput.setAttribute(
                "aria-required",
                String(isNotApplicable)
            );
        };

        yesInput.addEventListener(
            "change",
            updateReasonState
        );

        notApplicableInput.addEventListener(
            "change",
            () => {
                updateReasonState();

                if (notApplicableInput.checked) {
                    reasonInput.focus();
                }
            }
        );

        updateReasonState();
    });


    const errorSummary = document.querySelector(
        "#checklist-error-summary"
    );

    if (errorSummary) {
        errorSummary.focus();
    }


    const dialog = document.querySelector(
        "#checklist-submit-dialog"
    );

    const cancelButton = dialog?.querySelector(
        "[data-dialog-cancel]"
    );

    const confirmButton = dialog?.querySelector(
        "[data-dialog-confirm]"
    );

    const submitButton = form.querySelector(
        'input[type="submit"], button[type="submit"]'
    );

    let submissionConfirmed = false;


    form.addEventListener("submit", (event) => {
        if (submissionConfirmed) {
            return;
        }

        if (
            !dialog
            || typeof dialog.showModal !== "function"
        ) {
            return;
        }

        event.preventDefault();
        dialog.showModal();
    });


    cancelButton?.addEventListener("click", () => {
        dialog.close();
        submitButton?.focus();
    });


    confirmButton?.addEventListener("click", () => {
        submissionConfirmed = true;
        dialog.close();

        if (typeof form.requestSubmit === "function") {
            form.requestSubmit(submitButton);
        } else {
            form.submit();
        }
    });


    dialog?.addEventListener("cancel", () => {
        submitButton?.focus();
    });
});