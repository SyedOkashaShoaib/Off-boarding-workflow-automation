/* ------------------------------------------------------------
   Compact response selector
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
    display: inline-grid;
    grid-template-columns:
        minmax(92px, 108px)
        minmax(92px, 108px)
        minmax(148px, 176px);
    gap: 6px;
    max-width: 100%;
}

.response-option {
    position: relative;
    display: block;
    min-width: 0;
    margin: 0;
    padding: 0;
    background: transparent;
    border: 0;
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
}

.response-option__content {
    display: flex;
    min-height: 40px;
    height: 40px;
    align-items: center;
    justify-content: center;
    gap: 7px;
    padding: 0 12px;
    color: #263b4b;
    background:
        linear-gradient(
            to bottom,
            #ffffff 0%,
            #f8fbfd 48%,
            #e6eef4 100%
        );
    border: 1px solid #9fb0bd;
    border-radius: var(--radius-small, 4px);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.96),
        0 1px 1px rgba(43, 70, 88, 0.08);
    font-size: 13px;
    line-height: 1;
    white-space: nowrap;
    transition:
        border-color 120ms ease,
        background 120ms ease,
        box-shadow 120ms ease;
}

.response-option__content strong {
    font-size: 13px;
    font-weight: 650;
}

.response-option__indicator {
    display: block;
    flex: 0 0 14px;
    width: 14px;
    height: 14px;
    background: #ffffff;
    border: 1px solid #8498a7;
    border-radius: 50%;
    box-shadow:
        inset 0 1px 1px rgba(43, 67, 84, 0.10);
}

.response-option:hover .response-option__content {
    background:
        linear-gradient(
            to bottom,
            #ffffff,
            #e8f3fa
        );
    border-color: #6f96b0;
}

.response-option input:focus-visible
    + .response-option__content {
    outline: 3px solid rgba(43, 105, 155, 0.24);
    outline-offset: 2px;
}

.response-option input:checked
    + .response-option__content,
.response-option--selected
    .response-option__content {
    color: #173f5c;
    background:
        linear-gradient(
            to bottom,
            #fbfeff 0%,
            #e8f4fb 48%,
            #d4e8f5 100%
        );
    border-color: #4f84a8;
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.98),
        inset 0 0 0 1px rgba(107, 163, 200, 0.36),
        0 1px 2px rgba(40, 79, 106, 0.12);
}

.response-option input:checked
    + .response-option__content
    .response-option__indicator,
.response-option--selected
    .response-option__indicator {
    background: #3d7da7;
    border-color: #2f668b;
    box-shadow:
        inset 0 0 0 3px #edf7fc,
        inset 0 1px 1px rgba(20, 57, 82, 0.20);
}