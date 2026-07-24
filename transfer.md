const form = document.querySelector("[data-checklist-form]");
const dialog = document.querySelector("#checklist-submit-dialog");

if (!form) {
    return;
}

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

    if (
        dialog
        && typeof dialog.showModal === "function"
    ) {
        event.preventDefault();
        dialog.showModal();
        cancelButton?.focus();
        return;
    }

    /*
     * Fallback for a browser without <dialog> support.
     */
    const confirmed = window.confirm(
        "Submit this checklist? The responses cannot currently be edited."
    );

    if (!confirmed) {
        event.preventDefault();
    }
});

cancelButton?.addEventListener("click", () => {
    dialog.close();
    submitButton?.focus();
});

confirmButton?.addEventListener("click", () => {
    submissionConfirmed = true;

    confirmButton.disabled = true;
    confirmButton.textContent = "Submitting…";

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