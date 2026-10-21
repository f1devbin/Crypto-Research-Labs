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
OPENAI_MODEL = None   # discovered from the provider's /models list (free models get renamed and retired)
# preferred free chat models, best first (substring match against the provider's model ids)
PREFERRED = ["gpt-oss-120b", "llama-4-maverick", "kimi-k2", "llama-3.3-70b", "qwen3-32b", "gpt-oss-20b",
             "llama-4-scout", "gemma2-9b", "llama-3.1-8b"]
NOT_CHAT = ("whisper", "tts", "guard", "embed", "playai", "orpheus", "compound", "audio", "vision-preview")
_discovered: str | None = None


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


def _base() -> str:
    return (os.environ.get("CRL_LLM_BASE_URL") or OPENAI_BASE).rstrip("/")


def pick_model(ids: list[str]) -> str | None:
    chat = [m for m in ids if not any(x in m.lower() for x in NOT_CHAT)]
    for pref in PREFERRED:
        hit = sorted(m for m in chat if pref in m.lower())
        if hit:
            return hit[0]
    return sorted(chat)[0] if chat else None


def _discover() -> str:
    global _discovered
    if _discovered is None:
        req = urllib.request.Request(f"{_base()}/models", headers={
            "authorization": f"Bearer {os.environ['LLM_API_KEY']}", "user-agent": "crl/0.2"})
        with urllib.request.urlopen(req, timeout=30) as r:
            ids = [m.get("id", "") for m in json.loads(r.read()).get("data", []) if m.get("active", True)]
        _discovered = pick_model(ids)
        if not _discovered:
            raise LLMUnavailable("the provider lists no chat models; set CRL_LLM_MODEL")
    return _discovered


def model_name() -> str:
    if os.environ.get("CRL_LLM_MODEL"):
        return os.environ["CRL_LLM_MODEL"]
    if provider() == "openai":
        return _discover()
    return ANTHROPIC_MODEL


def _post(url: str, body: dict, headers: dict, timeout: int) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json", "user-agent": "crl/0.2", **headers})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def complete(system: str, prompt: str, max_tokens: int = 4000, timeout: int = 180) -> str:
    kind = provider()
    if kind == "openai":
        data = _post(f"{_base()}/chat/completions",
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
