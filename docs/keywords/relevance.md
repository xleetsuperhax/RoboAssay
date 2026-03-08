# Relevance Keywords

Assert that an LLM response is relevant to a topic, answers a question, or addresses all parts of a multi-part question.

---

## Response Should Be Relevant To

**Arguments:** `response`, `topic`

Asserts that the response is on-topic and relevant to the specified topic. Fails if the response goes off-topic or is unrelated.

```robot
Response Should Be Relevant To    ${response}    refund policy
Response Should Be Relevant To    ${response}    Python programming
Response Should Be Relevant To    ${response}    troubleshooting network connectivity
```

**Fails when:** The response discusses unrelated subjects, gives a generic non-answer, or clearly misses the topic.

---

## Response Should Answer Question

**Arguments:** `response`, `question`

Asserts that the response provides a clear, direct answer to the given question. The response doesn't need to be word-for-word correct — it just needs to address what was asked.

```robot
Response Should Answer Question    ${response}    What is your refund policy?
Response Should Answer Question    ${response}    How do I reset my password?
Response Should Answer Question    ${response}    What are the opening hours?
```

**Fails when:** The response acknowledges the question but doesn't actually answer it, or completely sidesteps it.

---

## Response Should Address All Parts

**Arguments:** `response`, `question`

Asserts that the response addresses every distinct part of a multi-part question. Useful for complex questions with multiple sub-questions.

```robot
Response Should Address All Parts    ${response}
...    What is the return window and what refund amount is offered?

Response Should Address All Parts    ${response}
...    What are the opening hours, location, and phone number?
```

**Fails when:** The response answers some parts of the question but ignores others.

---

## Full Example

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

Test Response Addresses All Parts
    Response Should Address All Parts    ${RESPONSE}
    ...    What is the return window and what kind of refund is offered?
```
