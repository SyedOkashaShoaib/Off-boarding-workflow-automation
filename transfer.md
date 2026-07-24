.confirmation-dialog {
    width: min(500px, calc(100vw - 32px));
    padding: 0;
    overflow: hidden;
    color: var(--text-primary);
    background: #f7fafc;
    border: 1px solid #496c84;
    border-radius: var(--radius-medium);
    box-shadow:
        0 18px 50px rgba(17, 38, 54, 0.40);
}

.confirmation-dialog::backdrop {
    background: rgba(25, 43, 56, 0.48);
    backdrop-filter: blur(1px);
}

.confirmation-dialog__header {
    padding: 11px 14px;
    color: var(--aero-header-text, #29485d);
    background: var(
        --aero-panel-header-background,
        linear-gradient(to bottom, #f9fcfe, #dce8f1)
    );
    border-bottom: 1px solid var(--border-medium);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.98),
        inset 0 -1px 0 rgba(43, 72, 93, 0.13);
}

.confirmation-dialog__header h2 {
    margin: 0;
    color: inherit;
    font-size: 17px;
}

.confirmation-dialog__body {
    padding: 18px;
}

.confirmation-dialog__body p {
    margin: 0;
}

.confirmation-dialog__body p + p {
    margin-top: 10px;
    color: var(--text-secondary);
}

.confirmation-dialog__actions {
    display: flex;
    justify-content: flex-end;
    gap: 9px;
    padding: 12px 15px;
    background: #e8eef2;
    border-top: 1px solid #b6c4ce;
}