"""Tests for the conversation helper keyword module."""

from RoboAssay.utils.conversation import (
    add_assistant_turn,
    add_user_turn,
    start_conversation,
)


class TestStartConversation:
    def test_returns_empty_list(self):
        result = start_conversation()
        assert result == []

    def test_returns_new_list_each_call(self):
        first = start_conversation()
        second = start_conversation()
        assert first is not second


class TestAddUserTurn:
    def test_appends_user_turn(self):
        conversation = start_conversation()
        result = add_user_turn(conversation, "Hello, how are you?")
        assert len(result) == 1
        assert result[0] == {"role": "user", "content": "Hello, how are you?"}

    def test_returns_same_list(self):
        conversation = start_conversation()
        result = add_user_turn(conversation, "Hello")
        assert result is conversation


class TestAddAssistantTurn:
    def test_appends_assistant_turn(self):
        conversation = start_conversation()
        result = add_assistant_turn(conversation, "I am doing well, thank you!")
        assert len(result) == 1
        assert result[0] == {"role": "assistant", "content": "I am doing well, thank you!"}

    def test_returns_same_list(self):
        conversation = start_conversation()
        result = add_assistant_turn(conversation, "Hello")
        assert result is conversation


class TestConversationBuilding:
    def test_full_multi_turn_conversation(self):
        conversation = start_conversation()
        add_user_turn(conversation, "What is 2 + 2?")
        add_assistant_turn(conversation, "2 + 2 equals 4.")
        add_user_turn(conversation, "And 3 + 3?")
        add_assistant_turn(conversation, "3 + 3 equals 6.")

        assert len(conversation) == 4
        assert conversation[0] == {"role": "user", "content": "What is 2 + 2?"}
        assert conversation[1] == {"role": "assistant", "content": "2 + 2 equals 4."}
        assert conversation[2] == {"role": "user", "content": "And 3 + 3?"}
        assert conversation[3] == {"role": "assistant", "content": "3 + 3 equals 6."}

    def test_roles_alternate_correctly(self):
        conversation = start_conversation()
        add_user_turn(conversation, "First user message")
        add_assistant_turn(conversation, "First assistant reply")
        add_user_turn(conversation, "Second user message")

        roles = [turn["role"] for turn in conversation]
        assert roles == ["user", "assistant", "user"]
