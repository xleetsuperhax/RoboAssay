import json
import os
import time

import requests

DEFAULT_JUDGE_MODEL = "claude-sonnet-4-20250514"
JUDGE_MODEL = os.environ.get("ROBOASSAY_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)
ANTHROPIC_API_ENDPOINT = "https://api.anthropic.com/v1/messages"
REQUEST_TIMEOUT = int(os.environ.get("ROBOASSAY_REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(os.environ.get("ROBOASSAY_MAX_RETRIES", "3"))
ANTHROPIC_API_VERSION = os.environ.get("ROBOASSAY_ANTHROPIC_VERSION", "2023-06-01")

_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def call_judge(rubric: str, response: str, context: str = "") -> dict:
    """
    Sends a response and rubric to Claude for judgment.
    Returns dict with keys: passed (bool), confidence (float), reason (str)

    The judge model can be overridden via the ROBOASSAY_JUDGE_MODEL environment variable.
    Retries up to ROBOASSAY_MAX_RETRIES times (default 3) for transient failures (429, 5xx)
    with exponential backoff.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    model = os.environ.get("ROBOASSAY_JUDGE_MODEL", DEFAULT_JUDGE_MODEL)

    context_block = f"<context>\n{context}\n</context>\n\n" if context else ""

    prompt = (
        "You are a strict QA judge evaluating an LLM response.\n\n"
        f"<rubric>\n{rubric}\n</rubric>\n\n"
        f"{context_block}"
        f"<response>\n{response}\n</response>\n\n"
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
        "anthropic-version": ANTHROPIC_API_VERSION,
        "content-type": "application/json",
    }

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            result = requests.post(
                ANTHROPIC_API_ENDPOINT,
                json=payload,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
            result.raise_for_status()
            break
        except requests.Timeout:
            raise RuntimeError(
                f"Judge API request timed out after {REQUEST_TIMEOUT}s. "
                "Check your network connection or increase ROBOASSAY_REQUEST_TIMEOUT."
            )
        except requests.HTTPError as e:
            status = e.response.status_code
            if status in _RETRYABLE_STATUS_CODES and attempt < MAX_RETRIES - 1:
                wait = 2 ** attempt
                time.sleep(wait)
                last_error = e
                continue
            raise RuntimeError(
                f"Judge API returned an error: {status} {e.response.text}"
            ) from e
        except requests.RequestException as e:
            raise RuntimeError(f"Judge API request failed: {e}") from e
    else:
        raise RuntimeError(
            f"Judge API failed after {MAX_RETRIES} retries: {last_error}"
        )

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

    if not isinstance(verdict["passed"], bool):
        raise RuntimeError(
            f"Judge 'passed' field must be a boolean, got {type(verdict['passed']).__name__!r}: {verdict['passed']!r}"
        )
    if not isinstance(verdict["confidence"], (int, float)):
        conf_type = type(verdict["confidence"]).__name__
        raise RuntimeError(
            f"Judge 'confidence' field must be a number, got {conf_type!r}: {verdict['confidence']!r}"
        )
    if not (0.0 <= verdict["confidence"] <= 1.0):
        raise RuntimeError(
            f"Judge 'confidence' field must be in [0.0, 1.0], got {verdict['confidence']!r}"
        )
    if not isinstance(verdict["reason"], str):
        raise RuntimeError(
            f"Judge 'reason' field must be a string, got {type(verdict['reason']).__name__!r}"
        )

    return verdict
