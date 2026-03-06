# Safety Keywords

Keywords for asserting that LLM responses handle safety correctly — refusing harmful requests, not leaking secrets, and not wrongly refusing legitimate requests.

## Keywords

### Response Should Refuse
**Arguments:** `response`, `prohibited_action`

Asserts that the response refuses to perform the prohibited action.

```robot
Response Should Refuse    ${response}    creating malware
```

### Response Should Not Leak
**Arguments:** `response`, `secret_content`

Asserts that the response does not reveal secret content (e.g., system prompts, API keys).

```robot
Response Should Not Leak    ${response}    ${system_prompt}
```

### Response Should Not Contain Harmful Content
**Arguments:** `response`

Asserts that the response does not contain harmful content (hate speech, violence, etc.).

```robot
Response Should Not Contain Harmful Content    ${response}
```

### Response Should Not Be Wrongly Refused
**Arguments:** `response`, `legitimate_intent`

Asserts that a legitimate request was not incorrectly refused.

```robot
Response Should Not Be Wrongly Refused    ${response}    asking for cooking recipes
```
