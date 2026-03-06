# Persona & Tone Keywords

Keywords for asserting that LLM responses maintain the correct tone, persona, and language.

## Keywords

### Response Tone Should Match
**Arguments:** `response`, `expected_tone`

Asserts that the response matches the expected tone (e.g., "professional", "friendly", "formal").

```robot
Response Tone Should Match    ${response}    professional
```

### Response Should Stay In Persona
**Arguments:** `response`, `persona_description`

Asserts that the response stays in character with the described persona.

```robot
Response Should Stay In Persona    ${response}    a helpful pirate captain
```

### Response Language Should Be
**Arguments:** `response`, `expected_language`

Asserts that the response is written in the expected language.

```robot
Response Language Should Be    ${response}    Spanish
```
