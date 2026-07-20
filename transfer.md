/* ============================================================
   Case detail foundation
   ============================================================ */

.case-detail-page {
    display: grid;
    gap: 18px;
}


.detail-grid {
    display: grid;
    grid-template-columns:
        repeat(2, minmax(0, 1fr));
    gap: 14px 24px;
    margin: 0;
}


.detail-grid > div {
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-light);
}


.detail-grid dt {
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 600;
}


.detail-grid dd {
    margin: 4px 0 0;
    font-weight: 600;
    overflow-wrap: anywhere;
}


@media (max-width: 760px) {

    .detail-grid {
        grid-template-columns: 1fr;
    }

}