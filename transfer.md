<dialog
    id="checklist-submit-dialog"
    class="confirmation-dialog"
    aria-labelledby="checklist-submit-dialog-title"
    aria-describedby="checklist-submit-dialog-description"
>
    <header class="confirmation-dialog__header">
        <h2 id="checklist-submit-dialog-title">
            Submit checklist?
        </h2>
    </header>

    <div class="confirmation-dialog__body">
        <p id="checklist-submit-dialog-description">
            The responses will be recorded and the workflow will
            advance to the next configured phase.
        </p>

        <p>
            Submitted responses cannot currently be edited.
        </p>
    </div>

    <footer class="confirmation-dialog__actions">
        <button
            type="button"
            class="btn-secondary"
            data-dialog-cancel
        >
            Go Back and Review
        </button>

        <button
            type="button"
            class="btn-primary"
            data-dialog-confirm
        >
            Submit Checklist
        </button>
    </footer>
</dialog>