# Instruction Following Keywords

Assert that an LLM response follows a specific format, respects topic boundaries, or complies with a given instruction.

---

## Response Should Follow Format

**Arguments:** `response`, `format_instruction`

Asserts that the response follows the specified format instruction. Describe the format in plain language — the same way you'd describe it in a system prompt.

```robot
Response Should Follow Format    ${response}    respond in bullet points
Response Should Follow Format    ${response}    use a numbered list
Response Should Follow Format    ${response}    respond in exactly three sentences
Response Should Follow Format    ${response}    use markdown headers for each section
Response Should Follow Format    ${response}    respond with a JSON object
```

**Fails when:** The response ignores the format — for example, using prose paragraphs when bullet points were expected.

---

## Response Should Respect Topic Boundary

**Arguments:** `response`, `forbidden_topics`

Asserts that the response does not venture into forbidden topics. Useful for customer-facing bots that should stay on a specific domain.

```robot
Response Should Respect Topic Boundary    ${response}    politics, religion
Response Should Respect Topic Boundary    ${response}    competitor products
Response Should Respect Topic Boundary    ${response}    medical advice, legal advice
Response Should Respect Topic Boundary    ${response}    pricing, discounts
```

**Fails when:** The response discusses any of the specified forbidden topics.

---

## Response Should Comply With

**Arguments:** `response`, `instruction`

General-purpose keyword for asserting that a response complies with any given instruction. More flexible than the other two keywords.

```robot
Response Should Comply With    ${response}    always include a disclaimer at the end
Response Should Comply With    ${response}    never recommend specific brands
Response Should Comply With    ${response}    always suggest contacting support for account issues
Response Should Comply With    ${response}    start the response with a greeting
```

**Fails when:** The response fails to follow the specified instruction.

---

## Full Example

```robot
*** Settings ***
Library    RoboAssay

*** Variables ***
${RESPONSE}
...    Here are the steps to reset your password:
...    • Visit the login page
...    • Click "Forgot Password"
...    • Enter your email address
...    • Check your inbox for a reset link
...
...    For further assistance, please contact our support team.

*** Test Cases ***
Test Format Is Bullet Points
    Response Should Follow Format    ${RESPONSE}    respond in bullet points

Test No Forbidden Topics
    Response Should Respect Topic Boundary    ${RESPONSE}    politics, competitor products

Test Disclaimer Is Included
    Response Should Comply With    ${RESPONSE}    include a suggestion to contact support
```

---

## Tips

!!! tip "Combining Instructions"
    Use `Response Should Comply With` for any instruction that doesn't fit the other two keywords. It's the most flexible and can cover requirements like:

    - Style requirements ("don't use jargon")
    - Structural requirements ("always open with a summary")
    - Content requirements ("mention the warranty at least once")
