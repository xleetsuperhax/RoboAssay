import json
import os

import requests

JUDGE_MODEL = "claude-sonnet-4-20250514"
ANTHROPIC_API_ENDPOINT = "https://api.anthropic.com/v1/messages"


def call_judge(rubric: str, response: str, context: str = "") -> dict:
    """
    Sends a response and rubric to Claude for judgment.
    Returns dict with keys: passed (bool), confidence (float), reason (str)
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

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
        "model": JUDGE_MODEL,
        "max_tokens": 256,
        "messages": [{"role": "user", "content": prompt}],
    }

    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    result = requests.post(ANTHROPIC_API_ENDPOINT, json=payload, headers=headers)
    result.raise_for_status()

    text = result.json()["content"][0]["text"]
    return json.loads(text)
