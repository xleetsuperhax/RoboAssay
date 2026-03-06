# Groundedness Keywords

Keywords for asserting that LLM responses are grounded in provided context and do not hallucinate.

## Keywords

### Response Should Be Grounded In
**Arguments:** `response`, `context`

Asserts that every claim in the response is supported by the provided context.

```robot
Response Should Be Grounded In    ${response}    ${context}
```

### Response Should Not Hallucinate
**Arguments:** `response`, `context`

Asserts that the response does not contain hallucinated information beyond what the context provides.

```robot
Response Should Not Hallucinate    ${response}    ${context}
```

### Response Should Not Contradict
**Arguments:** `response`, `context`

Asserts that the response does not contradict any information in the provided context.

```robot
Response Should Not Contradict    ${response}    ${context}
```
