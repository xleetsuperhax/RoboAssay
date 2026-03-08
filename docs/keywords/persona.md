# Persona & Tone Keywords

Assert that an LLM response maintains the correct tone, stays in character with a defined persona, or is written in the expected language.

---

## Response Tone Should Match

**Arguments:** `response`, `expected_tone`

Asserts that the overall tone of the response matches the expected tone. The tone description is flexible — use natural language to describe what you expect.

```robot
Response Tone Should Match    ${response}    professional
Response Tone Should Match    ${response}    friendly and approachable
Response Tone Should Match    ${response}    formal and concise
Response Tone Should Match    ${response}    empathetic and supportive
Response Tone Should Match    ${response}    casual and conversational
```

**Fails when:** The response has a clearly different tone from what was expected (e.g., response is sarcastic when `formal` was expected).

---

## Response Should Stay In Persona

**Arguments:** `response`, `persona_description`

Asserts that the response stays in character with the described persona. The persona description can be as detailed as you like.

```robot
Response Should Stay In Persona    ${response}    a helpful pirate captain
Response Should Stay In Persona    ${response}    a friendly medical assistant who never gives diagnoses
Response Should Stay In Persona    ${response}    a formal 19th-century English butler
Response Should Stay In Persona    ${response}    an enthusiastic sports commentator
```

**Fails when:** The response breaks character — for example, a pirate persona that starts responding like a corporate FAQ.

---

## Response Language Should Be

**Arguments:** `response`, `expected_language`

Asserts that the response is written in the expected language.

```robot
Response Language Should Be    ${response}    Spanish
Response Language Should Be    ${response}    French
Response Language Should Be    ${response}    Japanese
Response Language Should Be    ${response}    English
```

**Fails when:** The response is in a different language than expected, or is a mix of languages when a single language was specified.

---

## Full Example

```robot
*** Settings ***
Library    RoboAssay

*** Variables ***
${RESPONSE}
...    Ahoy there, matey! Welcome aboard the Ship of Answers!
...    Ye be wonderin' about our return policy, aye?
...    Fear not — we offer 30 days to return yer treasure, no questions asked!

*** Test Cases ***
Test Pirate Persona Is Maintained
    Response Should Stay In Persona    ${RESPONSE}    a friendly pirate

Test Tone Is Appropriate
    Response Tone Should Match    ${RESPONSE}    playful and nautical-themed

Test Response Is In English
    Response Language Should Be    ${RESPONSE}    English
```

---

## Multi-language Example

```robot
*** Test Cases ***
Test Spanish Support Bot
    # Assume your LLM was prompted to respond in Spanish
    ${response}=    Call My LLM    Hola, ¿cuál es su política de devolución?
    Response Language Should Be             ${response}    Spanish
    Response Should Be Relevant To          ${response}    política de devolución
    Response Tone Should Match              ${response}    friendly and professional
```
