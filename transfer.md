@media (max-width: 1050px) {

    .checklist-record__heading {
        grid-template-columns:
            minmax(0, 1fr)
            auto;
    }


    .checklist-record__metadata {
        grid-column: 1 / -1;
        grid-row: 2;
    }

}


@media (max-width: 760px) {

    .checklist-record__heading {
        grid-template-columns: 1fr;
        align-items: start;
    }


    .checklist-record__metadata {
        grid-column: auto;
        grid-row: auto;
        grid-template-columns: 1fr;
        width: 100%;
    }


    .checklist-record__metadata dd {
        max-width: none;
    }


    .checklist-record__heading > .register-status {
        justify-self: start;
    }


    .audit-entry__heading {
        align-items: flex-start;
        flex-direction: column;
    }

}