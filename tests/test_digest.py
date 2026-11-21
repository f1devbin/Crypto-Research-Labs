"""The weekly digest: numbers must come from the facts, and causes only when the facts state them."""
import datetime as dt
import json

from crl.llm import digest as D


def test_numbers_compare_without_spaces():
    assert D._numbers("BTC +1.5 % and 0.2%") == {"1.5%", "0.2%"}


def test_invented_numbers_are_reported():
    assert D._invented("BTC rose 42 % and 13 coins passed", "BTC rose 1.5 % on 13 coins") == ["42%"]
    assert D._invented("fees 0.2% vs 0.4 %", "fees 0.2 % vs 0.4 %") == []


def test_prompt_forbids_causes_and_keeps_the_numbers(monkeypatch, tmp_path):
    calls = []

    def fake(system, user, max_tokens):
        calls.append((system, user))
        if system != D.SYSTEM:
            return "The week moved.\n\n- BTC rose 1.5 %\n\nNothing changed."
        if sum(1 for s, _ in calls if s == D.SYSTEM) == 1:
            return "The week moved.\n\n- BTC rose 42 %\n\nNothing changed."
        return "The week moved.\n\n- BTC rose 1.5 %\n\nNothing changed."

    written = {}
    monkeypatch.setattr(D.client, "complete", fake)
    monkeypatch.setattr(D.client, "available", lambda: True)
    monkeypatch.setattr(D.client, "model_name", lambda: "fake")
    monkeypatch.setattr(D, "collect", lambda days=7: "BTC +1.5 % this week")
    monkeypatch.setattr(D, "alert", lambda *a, **k: None)
    monkeypatch.setattr(D, "alert_lang", lambda: "en")
    monkeypatch.setattr(D, "job_summary", lambda *a, **k: None)
    monkeypatch.setattr(D, "write", lambda facts, texts, model, day, errors=None, warnings=None:
                        written.update(texts=texts, warnings=warnings or {}))
    assert D.main() == 0
    english = [u for s, u in calls if s == D.SYSTEM]
    assert len(english) == 2 and "not in the reports" in english[1]
    assert "42" not in written["texts"]["en"] and "1.5" in written["texts"]["en"]
    assert written["warnings"] == {}


def test_a_second_bad_draft_is_kept_but_reported(monkeypatch):
    def fake(system, user, max_tokens):
        if system != D.SYSTEM:
            return "text"
        return "The week moved.\n\n- BTC rose 42 %\n\nNothing changed."

    written = {}
    monkeypatch.setattr(D.client, "complete", fake)
    monkeypatch.setattr(D.client, "available", lambda: True)
    monkeypatch.setattr(D.client, "model_name", lambda: "fake")
    monkeypatch.setattr(D, "collect", lambda days=7: "BTC +1.5 % this week")
    monkeypatch.setattr(D, "alert", lambda *a, **k: None)
    monkeypatch.setattr(D, "alert_lang", lambda: "en")
    monkeypatch.setattr(D, "job_summary", lambda *a, **k: None)
    monkeypatch.setattr(D, "write", lambda facts, texts, model, day, errors=None, warnings=None:
                        written.update(texts=texts, warnings=warnings or {}))
    assert D.main() == 0
    assert "42" in written["texts"]["en"]
    assert written["warnings"]["en"].startswith("numbers not in the facts")


def test_meta_records_warnings(tmp_path):
    d = D.write("facts", {"en": "text"}, "m", dt.date(2026, 11, 16), root=tmp_path, warnings={"en": "x"})
    assert json.loads((d / "meta.json").read_text(encoding="utf-8"))["warnings"] == {"en": "x"}
