.checklist-record__heading {
    display: grid;
    grid-template-columns:
        minmax(0, 1fr)
        auto;
    gap: 2mm 5mm;
}


.checklist-record__metadata {
    grid-column: 1 / -1;
    grid-row: 2;
    grid-template-columns:
        repeat(2, minmax(0, 1fr));
    gap: 2mm 6mm;
}


.checklist-record__metadata dt {
    color: #222 !important;
    font-size: 7pt;
}


.checklist-record__metadata dd {
    max-width: none;
    color: #000 !important;
    font-size: 8pt;
}


.checklist-record__heading > .register-status {
    grid-column: 2;
    grid-row: 1;
    justify-self: end;
}


.checklist-responsible-employee__code {
    color: #222 !important;
}