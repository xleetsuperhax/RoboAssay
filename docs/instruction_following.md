# Instruction Following Keywords

Keywords for asserting that LLM responses follow specific instructions, formats, and topic boundaries.

## Keywords

### Response Should Follow Format
**Arguments:** `response`, `format_instruction`

Asserts that the response follows the specified format instruction.

```robot
Response Should Follow Format    ${response}    respond in bullet points
```

### Response Should Respect Topic Boundary
**Arguments:** `response`, `forbidden_topics`

Asserts that the response does not discuss forbidden topics.

```robot
Response Should Respect Topic Boundary    ${response}    politics, religion
```

### Response Should Comply With
**Arguments:** `response`, `instruction`

Asserts that the response complies with a given instruction.

```robot
Response Should Comply With    ${response}    always include a disclaimer
```
