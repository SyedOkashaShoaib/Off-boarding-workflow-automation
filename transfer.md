/* ============================================================
   Case detail records
   ============================================================ */

.panel__heading p {
    margin: 3px 0 0;
    color: var(--text-secondary);
    font-size: 12px;
}


.case-detail-checklists {
    display: grid;
    gap: 16px;
}


.checklist-record {
    overflow: hidden;
    border: 1px solid var(--border-light);
    border-radius: var(--radius-medium);
}


.checklist-record__heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 10px 13px;
    background: #edf3f7;
    border-bottom: 1px solid var(--border-light);
}


.checklist-record__heading h3 {
    margin: 0;
    font-size: 14px;
}


.checklist-record__heading p {
    margin: 2px 0 0;
    color: var(--text-secondary);
    font-size: 12px;
}


.checklist-record-table {
    min-width: 950px;
}


.checklist-item-section {
    display: block;
    margin-bottom: 3px;
    color: var(--text-secondary);
    font-size: 11px;
    font-weight: 600;
}


.checklist-result {
    display: inline-flex;
    min-height: 23px;
    align-items: center;
    padding: 2px 7px;
    border: 1px solid;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
}


.checklist-result--yes {
    color: var(--success-text);
    background: var(--success-background);
    border-color: var(--success-border);
}


.checklist-result--not_applicable {
    color: #536471;
    background: #eef2f4;
    border-color: #aab6be;
}


.approval-record {
    margin-top: 16px;
    padding: 13px 15px;
    background: #f5f8fa;
    border: 1px solid var(--border-light);
    border-radius: var(--radius-medium);
}


.approval-record h3 {
    margin: 0 0 6px;
    font-size: 14px;
}


.approval-record p {
    margin: 0;
    white-space: pre-line;
}


.case-detail-empty {
    padding: 24px 18px;
    text-align: center;
}


.case-detail-empty h3 {
    margin: 0 0 5px;
}


.case-detail-empty p {
    margin: 0;
    color: var(--text-secondary);
}


.audit-timeline {
    margin: 0;
    padding: 0;
    list-style: none;
}


.audit-entry {
    display: grid;
    grid-template-columns: 14px minmax(0, 1fr);
    gap: 10px;
    position: relative;
    padding: 0 0 18px;
}


.audit-entry:not(:last-child)::before {
    position: absolute;
    top: 12px;
    bottom: 0;
    left: 5px;
    width: 1px;
    background: var(--border-medium);
    content: "";
}


.audit-entry__marker {
    position: relative;
    z-index: 1;
    width: 11px;
    height: 11px;
    margin-top: 5px;
    background: #f7fbfd;
    border: 2px solid #5585a5;
    border-radius: 50%;
}


.audit-entry__content {
    min-width: 0;
    padding-bottom: 2px;
}


.audit-entry__heading {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 14px;
}


.audit-entry__heading time {
    flex: none;
    color: var(--text-secondary);
    font-size: 11px;
}


.audit-entry__actor {
    margin: 3px 0 0;
    color: var(--text-secondary);
    font-size: 12px;
}


.audit-entry__details {
    margin: 6px 0 0;
    white-space: pre-line;
    overflow-wrap: anywhere;
}


@media (max-width: 760px) {

    .checklist-record__heading,
    .audit-entry__heading {
        align-items: flex-start;
        flex-direction: column;
    }

}