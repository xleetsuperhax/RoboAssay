# Groundedness Keywords

Assert that an LLM response is grounded in provided context — it doesn't invent facts, doesn't contradict what it was told, and doesn't hallucinate.

These keywords are essential for RAG (Retrieval-Augmented Generation) systems, customer support bots, and any application where the LLM must stay within provided knowledge.

---

## Response Should Be Grounded In

**Arguments:** `response`, `context`

Asserts that every factual claim in the response is supported by the provided context. The response should not introduce facts, figures, or statements that aren't present in or directly inferable from the context.

```robot
${context}=    Set Variable    The company was founded in 2015. It has 500 employees.
Response Should Be Grounded In    ${response}    ${context}
```

**Fails when:** The response makes claims that go beyond what the context states.

---

## Response Should Not Hallucinate

**Arguments:** `response`, `context`

Asserts that the response does not contain hallucinated information — fabricated details not present in the context. This is a stricter, more focused check than groundedness.

```robot
${context}=    Set Variable    The product costs $49.99 and ships in 3-5 business days.
Response Should Not Hallucinate    ${response}    ${context}
```

**Fails when:** The response invents specific details like numbers, names, dates, or facts not found in the context.

---

## Response Should Not Contradict

**Arguments:** `response`, `context`

Asserts that the response does not contradict any information in the provided context. The response can omit information from the context, but it cannot state the opposite of what the context says.

```robot
${context}=    Set Variable    The office is open Monday through Friday, 9am to 5pm.
Response Should Not Contradict    ${response}    ${context}
```

**Fails when:** The response says something that directly conflicts with the context (e.g., says the office is open on weekends when the context says it isn't).

---

## Full Example

```robot
*** Settings ***
Library    RoboAssay

*** Variables ***
${CONTEXT}
...    The company was founded in 2015 by Jane Smith.
...    It has 500 employees and is headquartered in Austin, Texas.

${GROUNDED}      The company, founded in 2015, is based in Austin, Texas.
${HALLUCINATED}  The company was founded in 2015 and has over 1,000 employees across 5 offices.

*** Test Cases ***
Test Response Is Grounded
    Response Should Be Grounded In    ${GROUNDED}    ${CONTEXT}

Test Response Does Not Hallucinate
    Response Should Not Hallucinate    ${GROUNDED}    ${CONTEXT}

Test Response Does Not Contradict Context
    Response Should Not Contradict    ${GROUNDED}    ${CONTEXT}

Test Hallucinated Response Is Caught
    [Documentation]    This test is expected to fail — detects hallucination.
    [Tags]    expected-fail
    Response Should Not Hallucinate    ${HALLUCINATED}    ${CONTEXT}
```

---

## Tips

!!! tip "Groundedness vs. Hallucination"
    - **Grounded In** checks that everything said is *supported* by context.
    - **Not Hallucinate** checks that nothing *invented* was added.
    - **Not Contradict** checks that nothing *opposes* the context.

    For comprehensive RAG testing, use all three.
