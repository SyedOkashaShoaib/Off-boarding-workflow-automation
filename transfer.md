@media (max-width: 900px) {
    .assignment-details__grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
    }

    .checklist-item__fields {
        grid-template-columns: 1fr;
    }

    .reason-field {
        grid-column: auto;
        max-width: none;
    }

    .checklist-submit-panel {
        align-items: stretch;
        flex-direction: column;
    }
}


@media (max-width: 650px) {
    .task-record-grid,
    .assignment-details__grid,
    .checklist-recorded-response {
        grid-template-columns: 1fr;
    }

    .response-options {
        display: grid;
        grid-template-columns:
            repeat(3, minmax(0, 1fr));
        width: 100%;
    }

    .confirmation-dialog__actions {
        flex-wrap: wrap;
    }
}


@media (max-width: 480px) {
    .response-options {
        grid-template-columns: 1fr;
    }

    .response-option__content {
        justify-content: flex-start;
        padding-right: 14px;
        padding-left: 14px;
    }

    .confirmation-dialog__actions {
        align-items: stretch;
        flex-direction: column-reverse;
    }

    .confirmation-dialog__actions button {
        width: 100%;
    }
}