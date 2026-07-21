/* Prevent the checklist collection being moved as one large grid. */
.case-detail-checklist-section,
.case-detail-checklists,
.checklist-record {
    display: block !important;
}


.case-detail-checklist-section,
.case-detail-checklists,
.checklist-record,
.checklist-record-table,
.case-table-scroll {
    break-inside: auto !important;
    page-break-inside: auto !important;
}


.case-detail-checklists {
    margin: 0;
}


.checklist-record {
    margin: 0 3mm 4mm !important;
    overflow: visible !important;
}


/*
 * Keep each department heading with the beginning of its table,
 * but allow the table itself to continue across pages.
 */
.checklist-record__heading {
    break-after: avoid-page !important;
    page-break-after: avoid !important;
}


.checklist-record-table {
    display: table !important;
    width: 100% !important;
}


.checklist-record-table thead {
    display: table-header-group;
}


.checklist-record-table tbody {
    display: table-row-group;
}


/* Individual checklist rows should normally remain intact. */
.checklist-record-table tr {
    break-inside: avoid !important;
    page-break-inside: avoid !important;
}