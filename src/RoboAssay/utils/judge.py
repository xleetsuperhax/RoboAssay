import json
import os

import requests

DEFAULT_JUDGE_MODEL = "claude-sonnet-4-20250514"
JUDGE_MODEL = os.environ.get("ROBOASSAY_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)
ANTHROPIC_API_ENDPOINT = "https://api.anthropic.com/v1/messages"
REQUEST_TIMEOUT = 30


def call_judge(rubric: str, response: str, context: str = "") -> dict:
    """
    Sends a response and rubric to Claude for judgment.
    Returns dict with keys: passed (bool), confidence (float), reason (str)

    The judge model can be overridden via the ROBOASSAY_JUDGE_MODEL environment variable.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    model = os.environ.get("ROBOASSAY_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)

    context_block = f"CONTEXT:\n{context}\n" if context else ""

    prompt = (
        "You are a strict QA judge evaluating an LLM response.\n\n"
        f"RUBRIC:\n{rubric}\n\n"
        f"{context_block}"
        f"RESPONSE TO EVALUATE:\n{response}\n\n"
        'Respond ONLY with valid JSON in this exact format:\n'
        '{"passed": true or false, "confidence": 0.0 to 1.0, "reason": "one sentence explanation"}'
    )

    payload = {
        "model": model,
        "max_tokens": 256,
        "messages": [{"role": "user", "content": prompt}],
    }

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    try:
        result = requests.post(
            ANTHROPIC_API_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        result.raise_for_status()
    except requests.Timeout:
        raise RuntimeError(
            f"Judge API request timed out after {REQUEST_TIMEOUT}s. "
            "Check your network connection or increase REQUEST_TIMEOUT."
        )
    except requests.HTTPError as e:
        raise RuntimeError(
            f"Judge API returned an error: {e.response.status_code} {e.response.text}"
        ) from e
    except requests.RequestException as e:
        raise RuntimeError(f"Judge API request failed: {e}") from e

    try:
        text = result.json()["content"][0]["text"]
    except (KeyError, IndexError, ValueError) as e:
        raise RuntimeError(
            f"Unexpected response structure from judge API: {result.text!r}"
        ) from e

    try:
        verdict = json.loads(text)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Judge returned non-JSON output: {text!r}"
        ) from e

    missing = [k for k in ("passed", "confidence", "reason") if k not in verdict]
    if missing:
        raise RuntimeError(
            f"Judge response missing expected keys {missing}: {verdict!r}"
        )

    return verdict
