/* ============================================================
   Case printing controls
   ============================================================ */

.case-detail-actions {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 8px;
}


.case-print-header {
    display: none;
}


/* ============================================================
   Printed case record
   ============================================================ */

@page {
    size: A4 portrait;
    margin: 12mm;
}


@media print {

    html,
    body {
        width: auto;
        min-width: 0;
        margin: 0;
        padding: 0;
        color: #000;
        background: #fff;
        font-family: Arial, Helvetica, sans-serif;
        font-size: 9.5pt;
        line-height: 1.35;
    }


    *,
    *::before,
    *::after {
        box-shadow: none !important;
        text-shadow: none !important;
    }


    .skip-link,
    .application-header,
    .application-sidebar,
    .page-context,
    .system-messages,
    .application-status-bar,
    .case-detail-actions,
    .case-detail-audit-section {
        display: none !important;
    }


    .application-shell,
    .application-body,
    .application-workspace,
    .application-content {
        display: block !important;
        width: 100% !important;
        min-width: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
        color: #000 !important;
        background: #fff !important;
        border: 0 !important;
    }


    .case-print-header {
        display: block;
        margin: 0 0 7mm;
        padding: 0 0 4mm;
        border-bottom: 1.5px solid #000;
    }


    .case-print-header__identity {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 8mm;
    }


    .case-print-header__company {
        display: block;
        font-size: 15pt;
        line-height: 1.15;
    }


    .case-print-header__system {
        display: block;
        margin-top: 1mm;
        font-size: 9pt;
    }


    .case-print-header__document {
        font-size: 12pt;
        font-weight: 700;
        text-align: right;
    }


    .case-print-header__metadata {
        display: grid;
        grid-template-columns:
            repeat(4, minmax(0, 1fr));
        gap: 3mm 6mm;
        margin: 5mm 0 0;
    }


    .case-print-header__metadata > div {
        min-width: 0;
    }


    .case-print-header__metadata dt {
        margin: 0;
        font-size: 7.5pt;
        font-weight: 700;
        text-transform: uppercase;
    }


    .case-print-header__metadata dd {
        margin: 1mm 0 0;
        font-weight: 600;
        overflow-wrap: anywhere;
    }


    .case-detail-page {
        display: block;
    }


    .case-detail-page > .panel {
        margin: 0 0 5mm;
        overflow: visible;
        background: #fff !important;
        border: 1px solid #777;
        border-radius: 0;
    }


    .panel__heading {
        padding: 2.5mm 3mm;
        color: #000 !important;
        background: #eee !important;
        border-bottom: 1px solid #777;
    }


    .panel__heading h2 {
        margin: 0;
        color: #000 !important;
        font-size: 11pt;
        break-after: avoid-page;
        page-break-after: avoid;
    }


    .panel__heading p {
        margin: 1mm 0 0;
        color: #222 !important;
        font-size: 8pt;
    }


    .detail-grid {
        grid-template-columns:
            repeat(2, minmax(0, 1fr));
        gap: 0;
        padding: 2mm 3mm;
    }


    .detail-grid > div {
        min-height: 11mm;
        padding: 2mm 3mm;
        border-bottom: 1px solid #ccc;
        break-inside: avoid;
        page-break-inside: avoid;
    }


    .detail-grid dt {
        color: #222 !important;
        font-size: 7.5pt;
    }


    .detail-grid dd {
        margin-top: 1mm;
        color: #000 !important;
        font-size: 9pt;
    }


    .case-detail-empty {
        padding: 4mm;
    }


    .case-detail-empty h3 {
        font-size: 10pt;
    }


    .case-detail-empty p {
        color: #222 !important;
    }


    .case-table-scroll {
        overflow: visible !important;
    }


    .case-register-table,
    .checklist-record-table {
        width: 100% !important;
        min-width: 0 !important;
        table-layout: fixed;
        border-collapse: collapse;
    }


    .case-register-table thead {
        display: table-header-group;
    }


    .case-register-table tr {
        break-inside: avoid;
        page-break-inside: avoid;
    }


    .case-register-table th,
    .case-register-table td {
        padding: 1.8mm;
        color: #000 !important;
        background: #fff !important;
        border: 1px solid #999;
        font-size: 7.5pt;
        line-height: 1.25;
        white-space: normal;
        overflow-wrap: anywhere;
    }


    .case-register-table th {
        background: #eee !important;
        font-weight: 700;
    }


    .checklist-record {
        margin: 0 3mm 4mm;
        overflow: visible;
        border: 1px solid #777;
        border-radius: 0;
    }


    .checklist-record__heading {
        padding: 2mm 3mm;
        background: #eee !important;
        border-bottom: 1px solid #777;
        break-after: avoid-page;
        page-break-after: avoid;
    }


    .checklist-record__heading h3 {
        color: #000 !important;
        font-size: 10pt;
    }


    .checklist-record__heading p {
        color: #222 !important;
    }


    .register-status,
    .attention-indicator,
    .checklist-result {
        min-height: 0;
        padding: 0;
        color: #000 !important;
        background: transparent !important;
        border: 0;
        border-radius: 0;
        font-size: inherit;
        font-weight: 600;
        white-space: normal;
    }


    .approval-record {
        margin: 3mm;
        padding: 3mm;
        color: #000 !important;
        background: #fff !important;
        border: 1px solid #999;
        border-radius: 0;
        break-inside: avoid;
        page-break-inside: avoid;
    }


    a,
    a:visited {
        color: #000 !important;
        text-decoration: none !important;
    }


    h2,
    h3,
    thead {
        break-after: avoid-page;
        page-break-after: avoid;
    }

}