.checklist-sections {
    display: grid;
    gap: 1.5rem;
}

.checklist-section {
    overflow: hidden;
    border: 1px solid #b8c4cf;
    border-radius: 8px;
    background: #ffffff;
    box-shadow:
        0 1px 2px rgba(30, 45, 60, 0.08),
        0 8px 20px rgba(30, 45, 60, 0.05);
}

.checklist-section__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #cbd4dc;
    background:
        linear-gradient(
            180deg,
            #f8fbfd 0%,
            #e7edf2 100%
        );
}

.checklist-section__eyebrow {
    margin: 0 0 0.2rem;
    color: #526576;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.checklist-section__title {
    margin: 0;
    color: #1f2f3d;
    font-size: 1.1rem;
}

.checklist-section__count {
    flex: 0 0 auto;
    padding: 0.3rem 0.65rem;
    border: 1px solid #aebbc6;
    border-radius: 999px;
    background: #ffffff;
    color: #3f5364;
    font-size: 0.8rem;
    font-weight: 700;
}

.checklist-section__items {
    display: grid;
}

.checklist-item {
    padding: 1.25rem;
    border-bottom: 1px solid #d8e0e6;
}

.checklist-item:last-child {
    border-bottom: 0;
}

.checklist-item--invalid {
    background: #fff9f8;
    box-shadow:
        inset 4px 0 0 #a13a32;
}

.checklist-item__heading {
    display: grid;
    grid-template-columns: auto minmax(0, 1fr);
    gap: 0.75rem;
    align-items: start;
    margin-bottom: 1rem;
}

.checklist-item__number {
    display: grid;
    width: 1.8rem;
    height: 1.8rem;
    place-items: center;
    border: 1px solid #9fadb9;
    border-radius: 50%;
    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #e4ebf0 100%
        );
    color: #2f4353;
    font-size: 0.8rem;
    font-weight: 700;
}

.checklist-item__title {
    margin: 0;
    color: #172734;
    font-size: 1rem;
    line-height: 1.45;
}

.checklist-item__description {
    margin: 0.35rem 0 0;
    color: #566a7a;
    font-size: 0.9rem;
    line-height: 1.5;
}

.checklist-item__fields {
    display: grid;
    grid-template-columns:
        minmax(18rem, 1.3fr)
        minmax(13rem, 0.8fr);
    gap: 1rem;
    align-items: start;
}

.response-fieldset {
    min-width: 0;
    margin: 0;
    padding: 0;
    border: 0;
}

.response-options {
    display: grid;
    grid-template-columns: repeat(
        3,
        minmax(0, 1fr)
    );
    gap: 0.65rem;
}

.response-option {
    position: relative;
    display: block;
    min-width: 0;
    cursor: pointer;
}

.response-option input {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    opacity: 0;
    pointer-events: none;
}

.response-option__content {
    display: grid;
    gap: 0.2rem;
    height: 100%;
    padding: 0.75rem;
    border: 1px solid #aebbc6;
    border-radius: 6px;
    background:
        linear-gradient(
            180deg,
            #ffffff 0%,
            #edf2f5 100%
        );
    color: #263b4b;
    transition:
        border-color 120ms ease,
        box-shadow 120ms ease,
        transform 120ms ease;
}

.response-option__content strong {
    font-size: 0.9rem;
}

.response-option__content small {
    color: #5b6e7d;
    font-size: 0.78rem;
    line-height: 1.35;
}

.response-option:hover
.response-option__content {
    border-color: #738da2;
}

.response-option input:focus-visible
+ .response-option__content {
    outline: 3px solid rgba(43, 105, 155, 0.25);
    outline-offset: 2px;
}

.response-option--selected
.response-option__content {
    border-color: #356f9e;
    background:
        linear-gradient(
            180deg,
            #f7fcff 0%,
            #dcebf6 100%
        );
    box-shadow:
        inset 0 0 0 1px #75a6c8,
        0 2px 5px rgba(37, 77, 108, 0.12);
    transform: translateY(-1px);
}

.response-option input:disabled
+ .response-option__content {
    cursor: default;
    opacity: 0.75;
}

.form-group {
    min-width: 0;
}

.form-label {
    display: block;
    margin-bottom: 0.4rem;
    color: #233746;
    font-size: 0.88rem;
    font-weight: 700;
}

.required-marker {
    color: #8d2d27;
}

.form-control {
    box-sizing: border-box;
    width: 100%;
    min-height: 2.5rem;
    padding: 0.6rem 0.7rem;
    border: 1px solid #9eacb8;
    border-radius: 5px;
    background: #ffffff;
    color: #1d2d39;
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
    min-height: 5.5rem;
    resize: vertical;
}

.form-help {
    margin: 0.35rem 0 0;
    color: #657684;
    font-size: 0.78rem;
    line-height: 1.4;
}

.reason-field {
    grid-column: 1 / -1;
    max-width: 50rem;
}

.reason-field[hidden] {
    display: none;
}

.checklist-item__error {
    margin-top: 1rem;
    padding: 0.7rem 0.8rem;
    border: 1px solid #c89792;
    border-radius: 5px;
    background: #fff1ef;
    color: #762b26;
    font-size: 0.85rem;
    font-weight: 600;
}

.task-alert {
    margin-bottom: 1rem;
    padding: 0.9rem 1rem;
    border-radius: 6px;
}

.task-alert p {
    margin: 0.35rem 0 0;
}

.task-alert--error {
    border: 1px solid #c89792;
    background: #fff1ef;
    color: #762b26;
}

@media (max-width: 900px) {
    .checklist-item__fields {
        grid-template-columns: 1fr;
    }

    .response-options {
        grid-template-columns: 1fr;
    }

    .reason-field {
        grid-column: auto;
    }
}