# RoboAssay

**Robot Framework keyword library for testing LLM-powered applications.**

RoboAssay lets you write Robot Framework tests that assert semantic properties of LLM responses — using Claude as an AI judge under the hood. Instead of brittle string matching, you write human-readable assertions like:

```robot
Response Should Be Relevant To       ${response}    refund policy
Response Should Not Hallucinate      ${response}    ${context}
Response Should Refuse               ${response}    creating malware
Response Tone Should Match           ${response}    professional
```

---

## How It Works

RoboAssay is **response-only** — it does not call your application's LLM. Your test suite is responsible for calling your LLM and capturing the response string. RoboAssay then passes that response to Claude (acting as an AI judge), which evaluates it against a rubric and returns a pass/fail verdict.

```
Your test  →  calls your LLM  →  gets a response string
                                        ↓
                              RoboAssay evaluates it
                                        ↓
                              Pass or Fail (AssertionError)
```

---

## Features

<div class="grid cards" markdown>

- **22 built-in keywords** covering relevance, groundedness, safety, persona, instruction-following, consistency, and regression testing — plus 3 conversation-building helpers

- **AI-powered assertions** — no regex, no exact-match. Claude understands semantics.

- **Multi-turn conversation support** — test LLM behavior across full conversation histories

- **Regression baselines** — save a good response and detect future behavioral drift

- **Standard Robot Framework** — works with any RF runner, listener, or reporting tool

</div>

---

## Quick Example

```robot
*** Settings ***
Library    RoboAssay

*** Variables ***
${CONTEXT}      Our return window is 30 days from date of purchase. Full refunds only.
${RESPONSE}     You can return any item within 30 days for a full refund.

*** Test Cases ***
Validate Customer Support Response
    Response Should Be Relevant To        ${RESPONSE}    return policy
    Response Should Be Grounded In        ${RESPONSE}    ${CONTEXT}
    Response Should Not Hallucinate       ${RESPONSE}    ${CONTEXT}
    Response Tone Should Match            ${RESPONSE}    friendly
```

---

## Keyword Categories

| Category | Keywords | What It Tests |
|---|---|---|
| [Relevance](keywords/relevance.md) | 3 | Is the response on-topic and does it answer the question? |
| [Groundedness](keywords/groundedness.md) | 3 | Does it stick to facts in context, no hallucination? |
| [Safety](keywords/safety.md) | 4 | Refusals, no leaks, no harmful content, no over-refusal |
| [Persona & Tone](keywords/persona.md) | 3 | Tone, persona, and language compliance |
| [Instruction Following](keywords/instruction-following.md) | 3 | Format, topic boundaries, custom instructions |
| [Consistency](keywords/consistency.md) | 3 | Internal consistency and multi-turn coherence |
| [Regression](keywords/regression.md) | 3 | Detect behavioral drift against saved baselines |

---

## Installation

```bash
pip install robotframework-roboassay
```

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

→ [Full installation guide](installation.md)
