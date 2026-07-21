"use strict";


document.addEventListener("DOMContentLoaded", () => {
    const caseRows = document.querySelectorAll(
        ".case-register-row[data-case-url]"
    );

    const interactiveSelector = [
        "a",
        "button",
        "input",
        "select",
        "textarea",
        "label",
        "summary"
    ].join(", ");


    caseRows.forEach((row) => {
        const destination = row.dataset.caseUrl;

        if (!destination) {
            return;
        }

        row.classList.add(
            "case-register-row--clickable"
        );


        row.addEventListener("click", (event) => {
            /*
             * Normal links and controls must preserve their own
             * browser behaviour.
             */
            if (
                event.target.closest(
                    interactiveSelector
                )
            ) {
                return;
            }

            /*
             * Do not navigate when the user is selecting and
             * copying table text.
             */
            const selectedText = window
                .getSelection()
                ?.toString()
                .trim();

            if (selectedText) {
                return;
            }

            window.location.assign(
                destination
            );
        });
    });
});