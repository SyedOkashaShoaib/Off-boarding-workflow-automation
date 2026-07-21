/* ============================================================
   Case register navigation
   ============================================================ */

.case-number-link {
    display: inline-block;
    font-weight: 700;
    text-decoration: none;
}


.case-number-link:hover {
    text-decoration: underline;
}


.case-number-link:focus-visible {
    border-radius: 2px;
    outline: 2px solid #2e78a7;
    outline-offset: 2px;
}


.case-register-row--clickable {
    cursor: pointer;
}


.case-register-row--clickable:hover td {
    background: #f1f7fb;
}


.case-register-row--clickable:focus-within td {
    background: #edf5fa;
}


.case-register-table__action-column,
.case-register-table__action-cell {
    width: 1%;
    text-align: right;
    white-space: nowrap;
}


.case-register-view-link {
    display: inline-flex;
    min-height: 30px;
    align-items: center;
    justify-content: center;
    padding: 4px 10px;
    font-size: 12px;
    white-space: nowrap;
}