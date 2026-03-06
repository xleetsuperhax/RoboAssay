# RoboAssay

A Robot Framework keyword library for testing LLM-powered applications.

RoboAssay provides assertion-style keywords that validate LLM responses using an AI judge (Claude). It does **not** send prompts to any LLM — that is the responsibility of the test author. This library only receives response strings and asserts properties about them.

## Installation

```bash
pip install robotframework-roboassay
```

Or install from source:

```bash
pip install -e .
```

## Setup

Set your Anthropic API key as an environment variable:

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

## Quick Start

```robot
*** Settings ***
Library    RoboAssay

*** Variables ***
${RESPONSE}    Our refund policy allows returns within 30 days of purchase with a full refund.

*** Test Cases ***
Test Response Is Relevant
    Response Should Be Relevant To    ${RESPONSE}    refund policy

Test Response Answers The Question
    Response Should Answer Question    ${RESPONSE}    What is your refund policy?
```

## Keyword Categories

| Category | Module | Keywords |
|---|---|---|
| Relevance | `relevance.py` | Response Should Be Relevant To, Response Should Answer Question, Response Should Address All Parts |
| Groundedness | `groundedness.py` | Response Should Be Grounded In, Response Should Not Hallucinate, Response Should Not Contradict |
| Safety | `safety.py` | Response Should Refuse, Response Should Not Leak, Response Should Not Contain Harmful Content, Response Should Not Be Wrongly Refused |
| Persona & Tone | `persona.py` | Response Tone Should Match, Response Should Stay In Persona, Response Language Should Be |
| Instruction Following | `instruction_following.py` | Response Should Follow Format, Response Should Respect Topic Boundary, Response Should Comply With |
| Consistency | `consistency.py` | Response Should Not Contradict Itself, Conversation Should Be Consistent, Last Response Should Reference |
| Regression | `regression.py` | Response Should Match Baseline Semantically, Save Response As Baseline, Response Behavior Should Not Have Changed |

## Multi-Turn Testing

```robot
*** Test Cases ***
Test Conversation Consistency
    ${conv}=    Start Conversation
    ${conv}=    Add User Turn     ${conv}    What is your name?
    ${conv}=    Add Assistant Turn    ${conv}    My name is Alex.
    ${conv}=    Add User Turn     ${conv}    What did you say your name was?
    ${conv}=    Add Assistant Turn    ${conv}    My name is Alex, as I mentioned before.
    Conversation Should Be Consistent    ${conv}
```

## License

MIT
