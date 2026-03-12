# Quick Start

This guide walks you through your first RoboAssay test in under 5 minutes.

---

## 1. Install RoboAssay

```bash
pip install robotframework-roboassay
export ANTHROPIC_API_KEY=your-api-key-here
```

---

## 2. Write Your First Test

Create a file called `test_my_llm.robot`:

```robot
*** Settings ***
Library    RoboAssay

*** Variables ***
# In a real test, this would come from calling your LLM
${RESPONSE}    Our return policy allows returns within 30 days for a full refund.

*** Test Cases ***
My First RoboAssay Test
    Response Should Be Relevant To      ${RESPONSE}    return policy
    Response Should Answer Question     ${RESPONSE}    What is the return policy?
    Response Tone Should Match          ${RESPONSE}    professional
```

---

## 3. Run It

```bash
robot test_my_llm.robot
```

RoboAssay evaluates each keyword and Robot Framework reports the result:

```
==============================================================================
My First RoboAssay Test
==============================================================================
My First RoboAssay Test                                               | PASS |
------------------------------------------------------------------------------
test_my_llm                                                           | PASS |
1 test, 1 passed, 0 failed
```

---

## 4. Test a Real LLM Response

In practice, your test will call your application's LLM and capture the response. Here's a realistic example using a hypothetical keyword `Call My LLM`:

```robot
*** Settings ***
Library    RoboAssay
Library    MyApp.LLMClient    # your own library

*** Variables ***
${CONTEXT}    Refunds are processed within 5 business days. Returns must be unopened.

*** Test Cases ***
Customer Support Bot Validates Refund Question
    # Call your LLM and capture the response
    ${response}=    Call My LLM    What is your refund policy?

    # Assert properties of the response
    Response Should Be Relevant To      ${response}    refund policy
    Response Should Be Grounded In      ${response}    ${CONTEXT}
    Response Should Not Hallucinate     ${response}    ${CONTEXT}
    Response Tone Should Match          ${response}    helpful and professional
```

---

## 5. Test Multi-Turn Conversations

RoboAssay includes conversation helper keywords for testing multi-turn behavior:

```robot
*** Settings ***
Library    RoboAssay

*** Test Cases ***
Conversation Stays Consistent
    # Build a conversation history
    ${conv}=    Start Conversation
    ${conv}=    Add User Turn        ${conv}    My account number is 12345.
    ${conv}=    Add Assistant Turn   ${conv}    Got it, I can see your account.
    ${conv}=    Add User Turn        ${conv}    What account number did I give you?
    ${conv}=    Add Assistant Turn   ${conv}    You gave me account number 12345.

    # Assert the conversation is consistent
    Conversation Should Be Consistent       ${conv}
    Last Response Should Reference          ${conv}    12345
```

---

## What's Next

- Explore the full [keyword reference](keywords/relevance.md) for all 22 keywords
- Learn about [regression testing](keywords/regression.md) to catch behavioral drift
- See [multi-turn examples](examples/multi-turn.md) for conversation testing patterns

---

## How RoboAssay Evaluates

Each keyword sends the response (and any context) to Claude with a rubric. Claude returns:

```json
{
  "passed": true,
  "confidence": 0.95,
  "reason": "The response directly addresses the return policy..."
}
```

If `passed` is `false`, RoboAssay raises an `AssertionError` with the reason, which Robot Framework records as a test failure. The reason tells you *why* the assertion failed — far more useful than a regex that silently misses the point.
