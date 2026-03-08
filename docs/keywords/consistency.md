# Consistency Keywords

Assert that an LLM response is internally consistent, or that a multi-turn conversation is coherent throughout.

---

## Response Should Not Contradict Itself

**Arguments:** `response`

Asserts that a single response does not contain internal contradictions. Useful for catching responses that say one thing in one sentence and the opposite in another.

```robot
Response Should Not Contradict Itself    ${response}
```

**Fails when:** The response contains contradictory statements — for example, claiming a product is both available and out of stock in the same response.

---

## Conversation Should Be Consistent

**Arguments:** `conversation_history`

Asserts that a multi-turn conversation is consistent throughout — the assistant doesn't contradict information it gave in earlier turns.

Build the conversation history using the [conversation helpers](#conversation-helpers): `Start Conversation`, `Add User Turn`, and `Add Assistant Turn`.

```robot
${conv}=    Start Conversation
${conv}=    Add User Turn        ${conv}    What is the capital of France?
${conv}=    Add Assistant Turn   ${conv}    The capital of France is Paris.
${conv}=    Add User Turn        ${conv}    And Germany?
${conv}=    Add Assistant Turn   ${conv}    The capital of Germany is Berlin.
Conversation Should Be Consistent    ${conv}
```

**Fails when:** The assistant contradicts itself across turns (e.g., says the capital is Paris in turn 1, then claims it's Lyon in turn 3).

---

## Last Response Should Reference

**Arguments:** `conversation_history`, `expected_reference`

Asserts that the last assistant response in the conversation references specific content — typically content from earlier in the conversation. Useful for verifying that the model correctly retains and uses context.

```robot
${conv}=    Start Conversation
${conv}=    Add User Turn        ${conv}    My favorite color is blue.
${conv}=    Add Assistant Turn   ${conv}    That's a great choice! Blue is calming.
${conv}=    Add User Turn        ${conv}    What did I say my favorite color was?
${conv}=    Add Assistant Turn   ${conv}    You said your favorite color is blue.
Last Response Should Reference    ${conv}    blue
```

**Fails when:** The last response does not reference or acknowledge the expected content.

---

## Conversation Helpers

These helper keywords are used to build conversation history objects for the consistency keywords.

### Start Conversation

Returns an empty conversation history list.

```robot
${conv}=    Start Conversation
```

### Add User Turn

Appends a user message to the conversation and returns the updated history.

```robot
${conv}=    Add User Turn    ${conv}    Hello, can you help me?
```

### Add Assistant Turn

Appends an assistant message to the conversation and returns the updated history.

```robot
${conv}=    Add Assistant Turn    ${conv}    Of course! What do you need help with?
```

The internal format is a list of role/content pairs:

```json
[
  {"role": "user", "content": "Hello, can you help me?"},
  {"role": "assistant", "content": "Of course! What do you need help with?"}
]
```

---

## Full Example

```robot
*** Settings ***
Library    RoboAssay

*** Test Cases ***
Test Multi-Turn Consistency
    ${conv}=    Start Conversation
    ${conv}=    Add User Turn        ${conv}    My account number is 12345.
    ${conv}=    Add Assistant Turn   ${conv}    Got it — I can see your account 12345.
    ${conv}=    Add User Turn        ${conv}    What account number did I give you?
    ${conv}=    Add Assistant Turn   ${conv}    You gave me account number 12345.

    Conversation Should Be Consistent       ${conv}
    Last Response Should Reference          ${conv}    12345

Test Single Response Has No Internal Contradictions
    ${response}=    Set Variable
    ...    Our store is open 24 hours a day, seven days a week.
    ...    We are closed on Sundays.
    Response Should Not Contradict Itself    ${response}
```
