import datetime as dt
import json

from crl.schedule_gate import decide, digest_missed, forecast_logged_on

UTC = dt.timezone.utc
TUE_EARLY = dt.datetime(2026, 10, 27, 3, 20, tzinfo=UTC)
TUE_LAST = dt.datetime(2026, 10, 27, 11, 20, tzinfo=UTC)
MON = dt.datetime(2026, 10, 26, 5, 0, tzinfo=UTC)


def test_waits_for_late_sources_until_the_last_slot():
    assert decide(TUE_EARLY, missing=["coinmetrics"], daily_today=False, weekly_today=False)[:2] == (False, False)
    assert decide(TUE_LAST, missing=["coinmetrics"], daily_today=False, weekly_today=False)[:2] == (True, False)


def test_first_ready_run_does_the_daily_job_once():
    assert decide(TUE_EARLY, missing=[], daily_today=False, weekly_today=False)[:2] == (True, False)
    assert decide(TUE_EARLY, missing=[], daily_today=True, weekly_today=False)[0] is False


def test_monday_runs_the_weekly_job_even_after_a_daily_build():
    assert decide(MON, missing=[], daily_today=True, weekly_today=False)[:2] == (True, True)
    assert decide(MON, missing=[], daily_today=True, weekly_today=True)[0] is False


def test_a_rebuild_after_a_merge_is_not_the_daily_job(tmp_path):
    log = tmp_path / "forecast_log.csv"
    log.write_text("published,date,decision_date,symbol\n2026-10-26T05:01:00Z,2026-10-26,2026-10-25,BTCUSDT\n")
    assert forecast_logged_on(dt.date(2026, 10, 26), log) and not forecast_logged_on(dt.date(2026, 10, 27), log)
    assert not forecast_logged_on(dt.date(2026, 10, 27), tmp_path / "missing.csv")
    # the site was rebuilt at night by a push, but today's forecast is not in: the first ready run still works
    assert decide(TUE_EARLY, missing=[], daily_today=False, weekly_today=False)[:2] == (True, False)


def test_a_missed_weekly_digest_makes_the_next_run_weekly(tmp_path):
    def digest(week, day):
        (tmp_path / week).mkdir()
        (tmp_path / week / "meta.json").write_text(json.dumps({"week": week, "date": day}))
    assert not digest_missed(dt.date(2026, 11, 4), tmp_path)  # no digest yet (no model configured): no catch-up
    digest("2026-W44", "2026-10-26")
    assert not digest_missed(dt.date(2026, 11, 2), tmp_path)  # Monday: the normal weekly run writes it
    assert digest_missed(dt.date(2026, 11, 4), tmp_path)
    wed = dt.datetime(2026, 11, 4, 5, 0, tzinfo=UTC)
    assert decide(wed, missing=[], daily_today=True, weekly_today=False, digest_late=True)[:2] == (True, True)
    assert decide(wed, missing=[], daily_today=True, weekly_today=True, digest_late=True)[0] is False
