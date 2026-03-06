from robot.api.deco import keyword


def create_conversation():
    """Create a new empty conversation history."""
    return []


def add_turn(history: list, role: str, content: str) -> list:
    """Add a turn to the conversation history."""
    history.append({"role": role, "content": content})
    return history


@keyword("Start Conversation")
def start_conversation() -> list:
    """Create and return a new conversation history."""
    return create_conversation()


@keyword("Add User Turn")
def add_user_turn(conversation: list, content: str) -> list:
    """Add a user turn to the conversation history."""
    return add_turn(conversation, "user", content)


@keyword("Add Assistant Turn")
def add_assistant_turn(conversation: list, content: str) -> list:
    """Add an assistant turn to the conversation history."""
    return add_turn(conversation, "assistant", content)
