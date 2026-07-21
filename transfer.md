<td class="case-register-table__action-cell">

    <a
        href="{{ url_for(
            'cases.case_detail',
            case_id=item.case_id
        ) }}"
        class="
            btn-secondary
            case-register-view-link
        "
        aria-label="View details for {{ item.case_number }}"
    >
        View details
    </a>

</td>