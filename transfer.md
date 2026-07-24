.visually-hidden {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    padding: 0 !important;
    margin: -1px !important;
    overflow: hidden !important;
    clip: rect(0, 0, 0, 0) !important;
    white-space: nowrap !important;
    border: 0 !important;
}


.checklist-guidance {
    display: flex;
    align-items: baseline;
    flex-wrap: wrap;
    gap: 3px 8px;
    margin: 0 0 14px;
    padding: 9px 12px;
    color: #344e60;
    background:
        linear-gradient(
            to bottom,
            #fbfdff,
            #edf4f8
        );
    border: 1px solid #bdccd7;
    border-radius: var(--radius-small, 4px);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.92);
    font-size: 12px;
}

.checklist-guidance strong {
    color: #29485d;
}

.checklist-guidance span {
    color: var(--text-secondary, #526875);
}