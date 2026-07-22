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

        const selectedResponse