"""Tiny LLM client (standard library only). Two kinds of providers:

* OpenAI-compatible chat API, e.g. Groq (free tier), OpenRouter, Google Gemini's OpenAI endpoint:
  LLM_API_KEY (+ optional CRL_LLM_BASE_URL, default Groq) and CRL_LLM_MODEL.
* Anthropic Messages API: ANTHROPIC_API_KEY (+ optional CRL_LLM_MODEL).

If both keys are set, LLM_API_KEY wins.
"""
import json
import os
import urllib.request

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-sonnet-5-5"
OPENAI_BASE = "https://api.groq.com/openai/v1"   # Groq: free tier, OpenAI-compatible
OPENAI_MODEL = "llama-3.3-70b-versatile"


class LLMUnavailable(RuntimeError):
    pass


def provider() -> str | None:
    if os.environ.get("LLM_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    return None


def available() -> bool:
    return provider() is not None


def model_name() -> str:
    default = OPENAI_MODEL if provider() == "openai" else ANTHROPIC_MODEL
    return os.environ.get("CRL_LLM_MODEL") or default


def _post(url: str, body: dict, headers: dict, timeout: int) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json", "user-agent": "crl/0.2", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def complete(system: str, prompt: str, max_tokens: int = 4000, timeout: int = 180) -> str:
    kind = provider()
    if kind == "openai":
        base = (os.environ.get("CRL_LLM_BASE_URL") or OPENAI_BASE).rstrip("/")
        data = _post(f"{base}/chat/completions",
                     {"model": model_name(), "max_tokens": max_tokens, "temperature": 0.3,
                      "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]},
                     {"authorization": f"Bearer {os.environ['LLM_API_KEY']}"}, timeout)
        return data["choices"][0]["message"]["content"] or ""
    if kind == "anthropic":
        data = _post(ANTHROPIC_URL,
                     {"model": model_name(), "max_tokens": max_tokens, "system": system,
                      "messages": [{"role": "user", "content": prompt}]},
                     {"x-api-key": os.environ["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01"}, timeout)
        return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    raise LLMUnavailable("set LLM_API_KEY (free OpenAI-compatible provider, e.g. Groq) or ANTHROPIC_API_KEY")
