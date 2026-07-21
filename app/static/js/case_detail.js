"use strict";

document.addEventListener("DOMContentLoaded", () => { const printButton = document.querySelector( "[data-print-case]" );

const generatedAtElement = document.querySelector(
    "[data-print-generated-at]"
);

if (!printButton) {
    return;
}


const originalDocumentTitle = document.title;

const caseNumber = (
    printButton.dataset.caseNumber
    || "Offboarding Case"
).trim();


const preparePrintRecord = () => {
    const currentDate = new Date();

    if (generatedAtElement) {
        generatedAtElement.textContent = (
            new Intl.DateTimeFormat(
                "en-GB",
                {
                    dateStyle: "long",
                    timeStyle: "short"
                }
            ).format(currentDate)
        );
    }

    /*
     * Browsers commonly use the document title as the
     * suggested filename when saving the print output as PDF.
     */
    document.title = (
        `${caseNumber} - Offboarding Case Record`
    );
};


const restoreDocumentTitle = () => {
    document.title = originalDocumentTitle;
};


printButton.addEventListener("click", () => {
    preparePrintRecord();
    window.print();
});


/*
 * This also prepares the record when the user invokes printing
 * through Ctrl+P or the browser menu instead of the page button.
 */
window.addEventListener(
    "beforeprint",
    preparePrintRecord
);

window.addEventListener(
    "afterprint",
    restoreDocumentTitle
);

});