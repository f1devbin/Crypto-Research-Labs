import json

from crl.llm import client


def test_provider_choice(monkeypatch):
    for k in ("LLM_API_KEY", "ANTHROPIC_API_KEY", "CRL_LLM_MODEL", "CRL_LLM_BASE_URL"):
        monkeypatch.delenv(k, raising=False)
    assert not client.available()
    monkeypatch.setenv("ANTHROPIC_API_KEY", "a")
    assert client.provider() == "anthropic" and client.model_name() == client.ANTHROPIC_MODEL
    monkeypatch.setenv("LLM_API_KEY", "g")
    assert client.provider() == "openai" and client.model_name() == client.OPENAI_MODEL


def test_openai_compatible_request(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "k")
    monkeypatch.setenv("CRL_LLM_BASE_URL", "https://example.test/v1/")
    seen = {}

    class R:
        def __init__(self, req):
            seen["url"], seen["body"], seen["auth"] = req.full_url, json.loads(req.data), req.headers["Authorization"]

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"choices": [{"message": {"content": "hi"}}]}).encode()
    monkeypatch.setattr(client.urllib.request, "urlopen", lambda req, timeout: R(req))
    assert client.complete("sys", "user") == "hi"
    assert seen["url"] == "https://example.test/v1/chat/completions" and seen["auth"] == "Bearer k"
    assert seen["body"]["messages"][0] == {"role": "system", "content": "sys"}
