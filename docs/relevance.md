# Relevance Keywords

Keywords for asserting that LLM responses are relevant to a given topic or question.

## Keywords

### Response Should Be Relevant To
**Arguments:** `response`, `topic`

Asserts that the response is relevant to the specified topic.

```robot
Response Should Be Relevant To    ${response}    refund policy
```

### Response Should Answer Question
**Arguments:** `response`, `question`

Asserts that the response provides a clear answer to the given question.

```robot
Response Should Answer Question    ${response}    What is your refund policy?
```

### Response Should Address All Parts
**Arguments:** `response`, `question`

Asserts that the response addresses all parts of a multi-part question.

```robot
Response Should Address All Parts    ${response}    What is the return window and what refund is offered?
```
