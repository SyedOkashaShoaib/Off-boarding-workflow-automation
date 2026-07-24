"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector(
        "[data-checklist-form]"
    );

    if (!form) {
        return;
    }

    const checklistItems = form.querySelectorAll(
        "[data-checklist-item]"
    );


    /**
     * Synchronize one checklist item's response controls.
     *
     * The server remains authoritative. This function only:
     * - updates the selected response styling;
     * - shows or hides the conditional reason field;
     * - updates the reason field's validation state and wording.
     */
    function synchronizeChecklistItem(
        checklistItem,
        {
            clearReasonForYes = false,
        } = {}
    ) {
        const responseInputs = Array.from(
            checklistItem.querySelectorAll(
                "[data-response-option]"
            )
        );

        const selectedResponse = responseInputs.find(
            (input) => input.checked
        );

        const reasonContainer = checklistItem.querySelector(
            "[data-reason-container]"
        );

        const reasonInput = checklistItem.querySelector(
            "[data-reason-input]"
        );

        const reasonLabel = checklistItem.querySelector(
            "[data-reason-label]"
        );

        const reasonHint = checklistItem.querySelector(
            "[data-reason-hint]"
        );

        const selectedValue = selectedResponse
            ? selectedResponse.value
            : "";

        const reasonRequired = (
            selectedValue === "NO"
            || selectedValue === "NOT_APPLICABLE"
        );


        responseInputs.forEach((input) => {
            const option = input.closest(
                ".response-option"
            );

            if (!option) {
                return;
            }

            option.classList.toggle(
                "response-option--selected",
                input.checked
            );
        });


        if (!reasonContainer || !reasonInput) {
            return;
        }

        reasonContainer.hidden = !reasonRequired;
        reasonInput.disabled = !reasonRequired;
        reasonInput.required = reasonRequired;

        reasonInput.setAttribute(
            "aria-required",
            reasonRequired ? "true" : "false"
        );

        checklistItem.classList.toggle(
            "checklist-item--requires-reason",
            reasonRequired
        );


        if (
            selectedValue === "YES"
            && clearReasonForYes
        ) {
            reasonInput.value = "";
        }


        if (reasonLabel) {
            if (selectedValue === "NO") {
                reasonLabel.textContent =
                    "Reason the action was not completed";
            } else if (
                selectedValue === "NOT_APPLICABLE"
            ) {
                reasonLabel.textContent =
                    "Reason the action does not apply";
            } else {
                reasonLabel.textContent = "Reason";
            }
        }


        if (reasonHint) {
            if (selectedValue === "NO") {
                reasonHint.textContent =
                    "Explain why the action was not completed.";
            } else if (
                selectedValue === "NOT_APPLICABLE"
            ) {
                reasonHint.textContent =
                    "Explain why this action does not apply.";
            } else {
                reasonHint.textContent =
                    "Required when the response is No "
                    + "or Not applicable.";
            }
        }
    }


    /**
     * Initialize every editable checklist item.
     */
    checklistItems.forEach((checklistItem) => {
        const responseInputs =
            checklistItem.querySelectorAll(
                "[data-response-option]"
            );

        synchronizeChecklistItem(checklistItem);

        responseInputs.forEach((input) => {
            input.addEventListener(
                "change",
                () => {
                    synchronizeChecklistItem(
                        checklistItem,
                        {
                            clearReasonForYes: true,
                        }
                    );
                }
            );
        });
    });


    /**
     * Move focus to the server-side validation summary when the
     * page has been rendered again with checklist errors.
     */
    const errorSummary = document.querySelector(
        "#checklist-error-summary"
    );

    if (errorSummary) {
        errorSummary.focus();
    }


    /**
     * Irreversible-submission confirmation.
     */
    const dialog = document.querySelector(
        "#checklist-submit-dialog"
    );

    const submitButton = form.querySelector(
        'input[type="submit"], button[type="submit"]'
    );

    const cancelButton = dialog?.querySelector(
        "[data-dialog-cancel]"
    );

    const confirmButton = dialog?.querySelector(
        "[data-dialog-confirm]"
    );

    let submissionConfirmed = false;


    form.addEventListener("submit", (event) => {
        if (submissionConfirmed) {
            return;
        }

        /*
         * Use the application dialog when supported.
         */
        if (
            dialog
            && typeof dialog.showModal === "function"
        ) {
            event.preventDefault();

            if (!dialog.open) {
                dialog.showModal();
            }

            cancelButton?.focus();
            return;
        }

        /*
         * Safe fallback for browsers without <dialog> support.
         */
        const confirmed = window.confirm(
            "Submit this checklist? "
            + "The responses cannot currently be edited."
        );

        if (!confirmed) {
            event.preventDefault();
            return;
        }

        submissionConfirmed = true;
    });


    cancelButton?.addEventListener(
        "click",
        () => {
            if (dialog?.open) {
                dialog.close();
            }

            submitButton?.focus();
        }
    );


    confirmButton?.addEventListener(
        "click",
        () => {
            submissionConfirmed = true;

            confirmButton.disabled = true;
            confirmButton.textContent = "Submitting…";

            if (dialog?.open) {
                dialog.close();
            }

            if (
                typeof form.requestSubmit === "function"
            ) {
                if (submitButton) {
                    form.requestSubmit(submitButton);
                } else {
                    form.requestSubmit();
                }

                return;
            }

            /*
             * Avoid form.submit being shadowed by a form control
             * whose name is "submit".
             */
            HTMLFormElement.prototype.submit.call(form);
        }
    );


    dialog?.addEventListener(
        "cancel",
        () => {
            submitButton?.focus();
        }
    );
});