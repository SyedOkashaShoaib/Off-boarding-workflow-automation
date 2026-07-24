/* ------------------------------------------------------------
   Task record
   ------------------------------------------------------------ */

.task-record-panel {
    margin: 0 0 18px;
    padding: 0;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid var(--border-medium, #9fb0bd);
    border-radius: var(--radius-medium, 6px);
    box-shadow:
        var(
            --shadow-panel,
            0 2px 5px rgba(44, 75, 96, 0.12)
        );
}


.task-record-panel__header {
    padding: 10px 14px;
    color: var(--aero-header-text, #29485d);
    background:
        var(
            --aero-panel-header-background,
            linear-gradient(
                to bottom,
                #f9fcfe,
                #dce8f1
            )
        );
    border-bottom: 1px solid
        var(--border-medium, #9fb0bd);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.98),
        inset 0 -1px 0 rgba(43, 72, 93, 0.13);
    text-shadow:
        0 1px 0 rgba(255, 255, 255, 0.84);
}


.task-record-panel__header h2 {
    margin: 0;
    color: inherit;
    font-size: 17px;
}


.task-record-grid {
    display: grid;
    grid-template-columns:
        repeat(2, minmax(0, 1fr));
    column-gap: 32px;
    margin: 0;
    padding: 4px 16px 16px;
}


.task-record-grid__item {
    min-width: 0;
    padding: 11px 0 10px;
    border-bottom: 1px solid #e2e9ee;
}


.task-record-grid__item dt {
    margin: 0 0 3px;
    color: var(--text-secondary, #526875);
    font-size: 12px;
    font-weight: 600;
}


.task-record-grid__item dd {
    margin: 0;
    overflow-wrap: anywhere;
    color: #263d4d;
    font-size: 14px;
    font-weight: 600;
    line-height: 1.4;
}


/* ------------------------------------------------------------
   Task status
   ------------------------------------------------------------ */

.status-badge {
    display: inline-flex;
    min-height: 24px;
    align-items: center;
    padding: 2px 9px;
    color: #304a5c;
    background: #e7eef3;
    border: 1px solid #91a5b4;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
}


.status-badge--in-progress {
    color: #234f71;
    background: #deedf8;
    border-color: #789fbc;
}


.status-badge--submitted,
.status-badge--completed,
.status-badge--approved {
    color: var(--success-text, #315d3b);
    background:
        var(--success-background, #e7f3e9);
    border-color:
        var(--success-border, #7ca287);
}


/* ------------------------------------------------------------
   Assignment details
   ------------------------------------------------------------ */

.assignment-details {
    margin-bottom: 18px;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid
        var(--border-medium, #9fb0bd);
    border-radius: var(--radius-medium, 6px);
    box-shadow:
        var(
            --shadow-panel,
            0 2px 5px rgba(44, 75, 96, 0.12)
        );
}


.assignment-details > h2 {
    margin: 0;
    padding: 10px 14px;
    color: #29465a;
    font-size: 17px;
}


.assignment-details__grid {
    display: grid;
    grid-template-columns:
        repeat(3, minmax(0, 1fr));
    gap: 14px 24px;
    margin: 0;
    padding: 16px;
}


.assignment-details__item {
    min-width: 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e9ee;
}


.assignment-details__item dt {
    margin-bottom: 3px;
    color: var(--text-secondary, #526875);
    font-size: 12px;
    font-weight: 600;
}


.assignment-details__item dd {
    margin: 0;
    overflow-wrap: anywhere;
    color: #263d4d;
    font-weight: 600;
}