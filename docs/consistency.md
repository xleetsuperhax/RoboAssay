# Consistency Keywords

Keywords for asserting internal consistency within single responses and across multi-turn conversations.

## Keywords

### Response Should Not Contradict Itself
**Arguments:** `response`

Asserts that the response does not contain internal contradictions.

```robot
Response Should Not Contradict Itself    ${response}
```

### Conversation Should Be Consistent
**Arguments:** `conversation_history`

Asserts that a multi-turn conversation is consistent throughout. Use with the conversation helper keywords.

```robot
${conv}=    Start Conversation
${conv}=    Add User Turn     ${conv}    What is your name?
${conv}=    Add Assistant Turn    ${conv}    My name is Alex.
${conv}=    Add User Turn     ${conv}    What did you say your name was?
${conv}=    Add Assistant Turn    ${conv}    My name is Alex.
Conversation Should Be Consistent    ${conv}
```

### Last Response Should Reference
**Arguments:** `conversation_history`, `expected_reference`

Asserts that the last response in a conversation references expected content.

```robot
Last Response Should Reference    ${conv}    blue
```
