/* ============================================================
   Shared structured panels and Aero headers
   ============================================================ */

/*
 * These components already provide their own body padding.
 * Reset the legacy global <section> padding so their headers
 * can meet the outer panel border.
 */
.information-card,
.checklist-section,
.panel,
.checklist-record {
    padding: 0;
    overflow: hidden;
}


/*
 * Visual treatment only. Individual page styles remain
 * responsible for flex/grid layout and component-specific spacing.
 */
.confirmation-heading,
.information-card__header,
.assignment-details > h2,
.checklist-section__header,
.case-filter-panel__heading,
.case-register-panel__heading,
.panel__heading,
.checklist-record__heading {
    color: var(--aero-header-text);
    background: var(--aero-panel-header-background);
    border-bottom: 1px solid var(--aero-header-border);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.98),
        inset 0 -1px 0 rgba(43, 72, 93, 0.13),
        0 1px 2px rgba(44, 75, 96, 0.08);
    text-shadow:
        0 1px 0 rgba(255, 255, 255, 0.84);
}