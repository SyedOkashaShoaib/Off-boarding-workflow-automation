"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const checklistItems = document.querySelectorAll(
        "[data-checklist-item]"
    );

    /**
     * Update one checklist item after its response changes.
     *
     * The server remains authoritative. This function only improves
     * the browser experience by showing the relevant reason field.
     */
    function synchronizeChecklistItem(
        checklistItem,
        {
            clearReasonForYes = false,
            focusReason = false,
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

            if (option) {
                option.classList.toggle(
                    "response-option--selected",
                    input.checked
                );
            }
        });

        if (!reasonContainer || !reasonInput) {
            return;
        }

        reasonContainer.hidden = !reasonRequired;

        reasonInput.required = (
            reasonRequired
            && !reasonInput.disabled
        );

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
                    "Reason for No";
            } else if (
                selectedValue === "NOT_APPLICABLE"
            ) {
                reasonLabel.textContent =
                    "Reason for Not applicable";
            } else {
                reasonLabel.textContent =
                    "Reason or explanation";
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

        if (
            reasonRequired
            && focusReason
            && !reasonInput.disabled
        ) {
            reasonInput.focus();
        }
    }

    checklistItems.forEach((checklistItem) => {
        const responseInputs = checklistItem.querySelectorAll(
            "[data-response-option]"
        );

        /*
         * Apply the correct initial state for:
         * - a new checklist;
         * - values restored after server validation;
         * - previously saved values.
         */
        synchronizeChecklistItem(
            checklistItem
        );

        responseInputs.forEach((input) => {
            input.addEventListener(
                "change",
                () => {
                    synchronizeChecklistItem(
                        checklistItem,
                        {
                            clearReasonForYes: true,
                            focusReason: (
                                input.value === "NO"
                                || input.value
                                    === "NOT_APPLICABLE"
                            ),
                        }
                    );
                }
            );
        });
    });
});