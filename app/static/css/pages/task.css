/* ============================================================
   Department task interface
   Matches app/templates/workflow/task_detail.html
   ============================================================ */

/* ------------------------------------------------------------
   Page heading and breadcrumbs
   ------------------------------------------------------------ */

.breadcrumbs {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 0 0 10px;
    padding: 0;
    color: var(--text-secondary, #526875);
    font-size: 12px;
    list-style: none;
}

.breadcrumbs__item + .breadcrumbs__item::before {
    margin-right: 6px;
    color: #7d8b95;
    content: "›";
}

.breadcrumbs__item--current {
    color: #29485e;
    font-weight: 600;
}

.task-access-workspace > h1 {
    margin: 0 0 5px;
    color: #20384a;
    font-size: clamp(26px, 3vw, 34px);
    line-height: 1.2;
}

.task-access-workspace > h1 + p {
    margin: 0 0 18px;
    color: var(--text-secondary, #526875);
    font-size: 14px;
}


/* ------------------------------------------------------------
   Task summary
   ------------------------------------------------------------ */

.task-summary-card {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(260px, 320px);
    grid-template-areas:
        "case metadata"
        "main metadata";
    gap: 8px 24px;
    margin-bottom: 18px;
    padding: 20px;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #edf5fa
        );
    border: 1px solid #7f9eb4;
    border-radius: var(--radius-medium, 6px);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.95),
        0 2px 5px rgba(44, 75, 96, 0.14);
}

.task-summary-card__case {
    grid-area: case;
}

.task-summary-card__label,
.task-summary-card__eyebrow {
    display: block;
    margin: 0 0 3px;
    color: var(--text-secondary, #526875);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.task-summary-card__case-number {
    display: block;
    color: #1f5577;
    font-size: 15px;
}

.task-summary-card__main {
    display: flex;
    grid-area: main;
    align-items: flex-start;
    justify-content: space-between;
    min-width: 0;
    gap: 18px;
    padding-top: 7px;
}

.task-summary-card__title {
    margin: 0 0 5px;
    color: #203d50;
    font-size: 21px;
    line-height: 1.3;
}

.task-summary-card__department {
    margin: 0;
    color: var(--text-secondary, #526875);
}

.task-summary-card__metadata {
    display: grid;
    grid-area: metadata;
    align-content: center;
    gap: 15px;
    margin: 0;
    padding-left: 22px;
    border-left: 1px solid #c7d5df;
}

.task-summary-card__metadata > div {
    display: grid;
    grid-template-columns: 84px minmax(0, 1fr);
    gap: 10px;
}

.task-summary-card__metadata dt {
    color: var(--text-secondary, #526875);
    font-size: 12px;
    font-weight: 600;
}

.task-summary-card__metadata dd {
    margin: 0;
    overflow-wrap: anywhere;
    font-weight: 600;
}

.status-badge {
    display: inline-flex;
    flex: 0 0 auto;
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
    background: var(--success-background, #e7f3e9);
    border-color: var(--success-border, #7ca287);
}


/* ------------------------------------------------------------
   Information cards
   ------------------------------------------------------------ */

.information-card,
.assignment-details {
    margin-bottom: 18px;
    overflow: hidden;
    background: #ffffff;
    border: 1px solid var(--border-medium, #9fb0bd);
    border-radius: var(--radius-medium, 6px);
    box-shadow: var(--shadow-panel, 0 2px 5px rgba(44, 75, 96, 0.12));
}

.information-card__header,
.assignment-details > h2 {
    margin: 0;
    padding: 10px 14px;
    background:
        linear-gradient(
            to bottom,
            #f9fcfe,
            #dce8f1
        );
    border-bottom: 1px solid var(--border-medium, #9fb0bd);
}

.information-card__header h2,
.assignment-details > h2 {
    margin: 0;
    color: #29465a;
    font-size: 17px;
}

.information-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px 24px;
    margin: 0;
    padding: 16px;
}

.information-grid__item {
    min-width: 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e9ee;
}

.information-grid__item dt {
    margin-bottom: 3px;
    color: var(--text-secondary, #526875);
    font-size: 12px;
    font-weight: 600;
}

.information-grid__item dd {
    margin: 0;
    overflow-wrap: anywhere;
    color: #263d4d;
    font-weight: 600;
}


/* ------------------------------------------------------------
   Alerts and validation
   ------------------------------------------------------------ */

.task-alert {
    display: flex;
    align-items: flex-start;
    gap: 13px;
    margin-bottom: 18px;
    padding: 15px 17px;
    border-radius: var(--radius-medium, 6px);
}

.task-alert__icon {
    display: grid;
    flex: 0 0 30px;
    width: 30px;
    height: 30px;
    place-items: center;
    color: #ffffff;
    background: #4d7d58;
    border-radius: 50%;
    font-weight: 700;
}

.task-alert h2 {
    margin: 1px 0 5px;
    color: inherit;
    font-size: 17px;
}

.task-alert p {
    margin: 3px 0;
}

.task-alert--success {
    color: var(--success-text, #315d3b);
    background: var(--success-background, #e7f3e9);
    border: 1px solid var(--success-border, #7ca287);
}

.task-alert--error {
    color: var(--error-text, #762b26);
    background: var(--error-background, #fff1ef);
    border: 1px solid var(--error-border, #c89792);
}

.validation-summary {
    margin-bottom: 18px;
    padding: 15px 17px;
    color: var(--error-text, #762b26);
    background: var(--error-background, #fff1ef);
    border: 1px solid var(--error-border, #c89792);
    border-radius: var(--radius-medium, 6px);
}

.validation-summary h2 {
    margin: 0 0 7px;
    color: inherit;
    font-size: 17px;
}

.validation-summary ul {
    margin: 0;
    padding-left: 22px;
}


/* ------------------------------------------------------------
   Checklist structure
   ------------------------------------------------------------ */

.checklist-form {
    max-width: none;
}

.checklist-sections {
    display: grid;
    gap: 18px;
}

.checklist-section {
    overflow: hidden;
    background: #ffffff;
    border: 1px solid var(--border-medium, #9fb0bd);
    border-radius: var(--radius-medium, 6px);
    box-shadow: var(--shadow-panel, 0 2px 5px rgba(44, 75, 96, 0.12));
}

.checklist-section__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 11px 14px;
    background:
        linear-gradient(
            to bottom,
            #f9fcfe,
            #dce8f1
        );
    border-bottom: 1px solid var(--border-medium, #9fb0bd);
}

.checklist-section__eyebrow {
    margin: 0 0 2px;
    color: var(--text-secondary, #526875);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.checklist-section__title {
    margin: 0;
    color: #29465a;
    font-size: 17px;
}

.checklist-section__count {
    flex: 0 0 auto;
    padding: 3px 9px;
    color: #3f5364;
    background: #ffffff;
    border: 1px solid #aebbc6;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
}

.checklist-section__items {
    padding: 0 16px;
}

.checklist-item {
    margin: 0;
    padding: 18px 0;
    outline: none;
}

.checklist-item + .checklist-item {
    border-top: 1px solid #dce4ea;
}

.checklist-item--invalid {
    margin-right: -16px;
    margin-left: -16px;
    padding-right: 16px;
    padding-left: 12px;
    background: #fff8f7;
    border-left: 4px solid var(--error-border, #c2554d);
}

.checklist-item__heading {
    display: flex;
    align-items: flex-start;
    gap: 11px;
    margin-bottom: 14px;
}

.checklist-item__number {
    display: grid;
    flex: 0 0 27px;
    width: 27px;
    height: 27px;
    place-items: center;
    color: #294d65;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #e3eef6
        );
    border: 1px solid #9cb5c7;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
}

.checklist-item__title {
    margin: 1px 0 3px;
    color: #263d4d;
    font-size: 15px;
    line-height: 1.45;
}

.checklist-item__required {
    color: #805044;
    font-size: 11px;
    font-weight: 600;
}

.checklist-item__fields {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(240px, 310px);
    gap: 14px 18px;
    margin-left: 38px;
    align-items: start;
}


/* ------------------------------------------------------------
   Response choices
   ------------------------------------------------------------ */

.response-fieldset {
    min-width: 0;
    margin: 0;
    padding: 0;
    background: transparent;
    border: 0;
    box-shadow: none;
}

.response-fieldset legend {
    padding: 0;
}

.response-options {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 9px;
    margin-top: 8px;
}

.response-option {
    position: relative;
    display: block;
    min-width: 0;
    min-height: 0;
    margin: 0;
    padding: 0;
    background: transparent;
    border: 0;
    border-radius: 0;
    box-shadow: none;
    cursor: pointer;
}

.response-option input {
    position: absolute;
    width: 1px;
    height: 1px;
    margin: 0;
    overflow: hidden;
    opacity: 0;
    pointer-events: none;
}

.response-option__content {
    display: flex;
    min-height: 70px;
    height: 100%;
    flex-direction: column;
    gap: 3px;
    padding: 10px 11px;
    color: #263b4b;
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #f0f5f8
        );
    border: 1px solid #a4b5c1;
    border-radius: var(--radius-small, 4px);
    transition:
        border-color 120ms ease,
        background-color 120ms ease,
        box-shadow 120ms ease,
        transform 120ms ease;
}

.response-option__content strong {
    font-size: 14px;
}

.response-option__content small {
    color: var(--text-secondary, #526875);
    font-size: 12px;
    font-weight: 400;
    line-height: 1.35;
}

.response-option:hover .response-option__content {
    background: #edf6fc;
    border-color: #6f99b6;
}

.response-option input:focus-visible + .response-option__content {
    outline: 3px solid rgba(43, 105, 155, 0.25);
    outline-offset: 2px;
}

.response-option input:checked + .response-option__content,
.response-option--selected .response-option__content {
    background:
        linear-gradient(
            to bottom,
            #f7fcff,
            #dcebf6
        );
    border-color: #356f9e;
    box-shadow:
        inset 0 0 0 1px #75a6c8,
        0 2px 5px rgba(37, 77, 108, 0.12);
    transform: translateY(-1px);
}


/* ------------------------------------------------------------
   Form fields
   ------------------------------------------------------------ */

.form-group {
    min-width: 0;
}

.form-label {
    display: block;
    margin-bottom: 5px;
    color: #233746;
    font-size: 12px;
    font-weight: 700;
}

.required-marker {
    color: #8d2d27;
}

.form-control {
    box-sizing: border-box;
    width: 100%;
    min-height: 40px;
    padding: 9px 10px;
    color: #1d2d39;
    background: #ffffff;
    border: 1px solid #9eacb8;
    border-radius: var(--radius-small, 4px);
    font: inherit;
}

.form-control:focus {
    border-color: #3977a7;
    outline: 3px solid rgba(57, 119, 167, 0.18);
}

.form-control[aria-invalid="true"] {
    border-color: #9d3932;
}

.form-control--textarea {
    min-height: 88px;
    resize: vertical;
}

.form-help {
    margin: 4px 0 0;
    color: var(--text-secondary, #526875);
    font-size: 11px;
    line-height: 1.4;
}

.reason-field {
    grid-column: 1 / -1;
    max-width: 760px;
}

.reason-field[hidden] {
    display: none;
}

.checklist-item__error {
    margin: 12px 0 0 38px;
    padding: 9px 11px;
    color: var(--error-text, #762b26);
    background: var(--error-background, #fff1ef);
    border: 1px solid var(--error-border, #c89792);
    border-radius: var(--radius-small, 4px);
    font-size: 12px;
    font-weight: 600;
}


/* ------------------------------------------------------------
   Read-only recorded responses
   ------------------------------------------------------------ */

.checklist-recorded-response {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px 18px;
    margin-left: 38px;
    padding: 13px;
    background: #f5f8fa;
    border: 1px solid #c7d3db;
    border-radius: var(--radius-small, 4px);
}

.checklist-recorded-response__item {
    min-width: 0;
}

.checklist-recorded-response__item--full {
    grid-column: 1 / -1;
    padding-top: 10px;
    border-top: 1px solid #d6e0e6;
}

.checklist-recorded-response__label {
    display: block;
    margin-bottom: 3px;
    color: var(--text-secondary, #526875);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.checklist-recorded-response p {
    margin: 3px 0 0;
}


/* ------------------------------------------------------------
   Submission panel and empty state
   ------------------------------------------------------------ */

.checklist-submit-panel {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 22px;
    margin-top: 20px;
    padding: 16px;
    background:
        linear-gradient(
            to bottom,
            #f9fbfc,
            #e3ebf0
        );
    border: 1px solid var(--border-medium, #9fb0bd);
    border-radius: var(--radius-medium, 6px);
}

.checklist-submit-panel h2 {
    margin: 0 0 4px;
    color: #29465a;
    font-size: 17px;
}

.checklist-submit-panel p {
    max-width: 760px;
    margin: 0;
    color: var(--text-secondary, #526875);
}

.checklist-submit-button {
    flex: 0 0 auto;
}

.empty-state {
    margin-bottom: 18px;
    padding: 20px;
    color: var(--error-text, #762b26);
    background: var(--error-background, #fff1ef);
    border: 1px solid var(--error-border, #c89792);
    border-radius: var(--radius-medium, 6px);
}

.empty-state h2 {
    margin-top: 0;
    color: inherit;
}


/* ------------------------------------------------------------
   Responsive behavior
   ------------------------------------------------------------ */

@media (max-width: 900px) {
    .task-summary-card {
        grid-template-columns: 1fr;
        grid-template-areas:
            "case"
            "main"
            "metadata";
    }

    .task-summary-card__metadata {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        padding-top: 15px;
        padding-left: 0;
        border-top: 1px solid #c7d5df;
        border-left: 0;
    }

    .task-summary-card__metadata > div {
        grid-template-columns: 1fr;
        gap: 2px;
    }

    .information-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
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
    .task-access-workspace {
        width: min(100% - 20px, 1180px);
        margin-top: 12px;
    }

    .task-summary-card__main {
        flex-direction: column;
    }

    .task-summary-card__metadata,
    .information-grid,
    .response-options,
    .checklist-recorded-response {
        grid-template-columns: 1fr;
    }

    .checklist-item__fields,
    .checklist-recorded-response,
    .checklist-item__error {
        margin-left: 0;
    }

    .checklist-recorded-response__item--full {
        grid-column: auto;
    }

    .checklist-item__heading {
        gap: 8px;
    }
}
