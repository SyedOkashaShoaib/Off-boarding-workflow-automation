<a
    href="{{ url_for(
        'cases.case_detail',
        case_id=item.case_id
    ) }}"
    class="case-number case-number-link"
    aria-label="View case {{ item.case_number }}"
>
    {{ item.case_number }}
</a>