/* Shared Aero-style header surfaces */
--aero-header-top: #f9fcfe;
--aero-header-middle: #edf5fa;
--aero-header-bottom: #dce8f1;
--aero-header-border: var(--border-medium);
--aero-header-text: #29485d;

--aero-panel-header-background:
    radial-gradient(
        145% 120% at 50% -55%,
        rgba(255, 255, 255, 0.98) 0%,
        rgba(255, 255, 255, 0.76) 37%,
        rgba(255, 255, 255, 0.20) 59%,
        rgba(255, 255, 255, 0) 72%
    ),
    linear-gradient(
        to bottom,
        var(--aero-header-top) 0%,
        var(--aero-header-middle) 48%,
        var(--aero-header-bottom) 100%
    );

--aero-table-header-background:
    linear-gradient(
        to bottom,
        rgba(255, 255, 255, 0.84) 0%,
        rgba(255, 255, 255, 0.42) 42%,
        rgba(255, 255, 255, 0.10) 43%,
        rgba(255, 255, 255, 0) 100%
    ),
    linear-gradient(
        to bottom,
        var(--aero-header-top) 0%,
        var(--aero-header-middle) 50%,
        var(--aero-header-bottom) 100%
    );