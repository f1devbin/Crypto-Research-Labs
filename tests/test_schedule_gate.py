import datetime as dt

from crl.schedule_gate import decide

UTC = dt.timezone.utc
TUE_EARLY = dt.datetime(2026, 10, 27, 3, 20, tzinfo=UTC)
TUE_LAST = dt.datetime(2026, 10, 27, 11, 20, tzinfo=UTC)
MON = dt.datetime(2026, 10, 26, 5, 0, tzinfo=UTC)


def test_waits_for_late_sources_until_the_last_slot():
    assert decide(TUE_EARLY, missing=["coinmetrics"], site_today=False, weekly_today=False)[:2] == (False, False)
    assert decide(TUE_LAST, missing=["coinmetrics"], site_today=False, weekly_today=False)[:2] == (True, False)


def test_first_ready_run_does_the_daily_job_once():
    assert decide(TUE_EARLY, missing=[], site_today=False, weekly_today=False)[:2] == (True, False)
    assert decide(TUE_EARLY, missing=[], site_today=True, weekly_today=False)[0] is False


def test_monday_runs_the_weekly_job_even_after_a_daily_build():
    assert decide(MON, missing=[], site_today=True, weekly_today=False)[:2] == (True, True)
    assert decide(MON, missing=[], site_today=True, weekly_today=True)[0] is False
