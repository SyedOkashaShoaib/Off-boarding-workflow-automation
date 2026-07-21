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

/*
 * Stores links temporarily stripped before printing.
 * A Map makes this safe when preparePrintRecord() is called
 * once by the button and again by the beforeprint event.
 */
const removedPrintLinks = new Map();


const removePrintableLinks = () => {
    const links = document.querySelectorAll(
        ".application-content a[href]"
    );

    links.forEach((link) => {
        if (!removedPrintLinks.has(link)) {
            removedPrintLinks.set(
                link,
                link.getAttribute("href")
            );
        }

        link.removeAttribute("href");
    });
};


const restorePrintableLinks = () => {
    removedPrintLinks.forEach(
        (href, link) => {
            if (href !== null) {
                link.setAttribute(
                    "href",
                    href
                );
            }
        }
    );

    removedPrintLinks.clear();
};


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

    document.title = (
        `${caseNumber} - Offboarding Case Record`
    );

    removePrintableLinks();
};


const restorePrintRecord = () => {
    document.title = originalDocumentTitle;
    restorePrintableLinks();
};


printButton.addEventListener(
    "click",
    () => {
        preparePrintRecord();
        window.print();
    }
);


window.addEventListener(
    "beforeprint",
    preparePrintRecord
);

window.addEventListener(
    "afterprint",
    restorePrintRecord
);

});