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
    display: grid;
    grid-template-columns:
        minmax(180px, 1fr)
        auto
        auto;
    align-items: center;
    gap: 16px 24px;
    padding: 11px 14px;
    background:
        linear-gradient(
            to bottom,
            #f6fafc,
            #e7eff4
        );
    border-bottom: 1px solid var(--border-light);
}


.checklist-record__identity {
    min-width: 0;
}


.checklist-record__identity h3 {
    margin: 0;
    color: #29465a;
    font-size: 14px;
}


.checklist-record__identity p {
    margin: 2px 0 0;
    color: var(--text-secondary);
    font-size: 12px;
}


.checklist-record__metadata {
    display: grid;
    grid-template-columns:
        repeat(2, minmax(140px, auto));
    gap: 8px 20px;
    margin: 0;
}


.checklist-record__metadata > div {
    min-width: 0;
}


.checklist-record__metadata dt {
    color: var(--text-secondary);
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}


.checklist-record__metadata dd {
    max-width: 260px;
    margin: 2px 0 0;
    overflow-wrap: anywhere;
    color: #263d4d;
    font-size: 12px;
    font-weight: 600;
}


.checklist-record__heading > .register-status {
    justify-self: end;
}


.checklist-record-table {
    width: 100%;
    min-width: 920px;
    table-layout: fixed;
}


.checklist-record-table__item-column {
    width: 44%;
}


.checklist-record-table__result-column {
    width: 12%;
}


.checklist-record-table__reason-column {
    width: 25%;
}


.checklist-record-table__employee-column {
    width: 19%;
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


.checklist-result--no {
    color: var(--error-text);
    background: var(--error-background);
    border-color: var(--error-border);
}


.checklist-result--not_applicable {
    color: #536471;
    background: #eef2f4;
    border-color: #aab6be;
}


.checklist-reason-cell {
    vertical-align: top;
}


.checklist-reason-text {
    display: block;
    white-space: pre-line;
    overflow-wrap: anywhere;
    line-height: 1.45;
}


.checklist-responsible-employee {
    vertical-align: top;
    overflow-wrap: anywhere;
}


.checklist-responsible-employee__name {
    display: block;
    color: #263d4d;
}


.checklist-responsible-employee__code {
    display: block;
    margin-top: 3px;
    color: var(--text-secondary);
    font-size: 11px;
    font-weight: 600;
}