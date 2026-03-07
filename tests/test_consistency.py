"""Tests for the consistency keyword module."""

from unittest.mock import patch

import pytest

from RoboAssay.consistency import (
    response_should_not_contradict_itself,
    conversation_should_be_consistent,
    last_response_should_reference,
)


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


class TestResponseShouldNotContradictItself:
    def test_passes_when_internally_consistent(self, mock_env):
        with patch("RoboAssay.consistency.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.94, "reason": "No internal contradictions found"}
            response_should_not_contradict_itself(
                "Python is a dynamically typed language. It supports multiple programming paradigms including object-oriented and functional styles."
            )

    def test_fails_when_self_contradicting(self, mock_env):
        with patch("RoboAssay.consistency.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.91, "reason": "Response states Python is both compiled and interpreted"}
            with pytest.raises(AssertionError, match="internal contradictions"):
                response_should_not_contradict_itself(
                    "Python is a compiled language. However, Python is also an interpreted language that does not require compilation."
                )


class TestConversationShouldBeConsistent:
    def test_passes_when_conversation_consistent(self, mock_env):
        with patch("RoboAssay.consistency.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.92, "reason": "Assistant maintains consistent facts across turns"}
            conversation = [
                {"role": "user", "content": "What is the capital of France?"},
                {"role": "assistant", "content": "The capital of France is Paris."},
                {"role": "user", "content": "And what country is Paris in?"},
                {"role": "assistant", "content": "Paris is in France."},
            ]
            conversation_should_be_consistent(conversation)

    def test_fails_when_conversation_inconsistent(self, mock_env):
        with patch("RoboAssay.consistency.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.89, "reason": "Assistant contradicts itself between turns"}
            with pytest.raises(AssertionError, match="Conversation contains inconsistencies"):
                conversation = [
                    {"role": "user", "content": "What is the capital of France?"},
                    {"role": "assistant", "content": "The capital of France is Paris."},
                    {"role": "user", "content": "Are you sure?"},
                    {"role": "assistant", "content": "Actually, the capital of France is Lyon, not Paris."},
                ]
                conversation_should_be_consistent(conversation)


class TestLastResponseShouldReference:
    def test_passes_when_reference_present(self, mock_env):
        with patch("RoboAssay.consistency.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.93, "reason": "Last response references the user's name"}
            conversation = [
                {"role": "user", "content": "My name is Alice."},
                {"role": "assistant", "content": "Nice to meet you, Alice! How can I help you?"},
            ]
            last_response_should_reference(conversation, "Alice")

    def test_fails_when_reference_missing(self, mock_env):
        with patch("RoboAssay.consistency.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.87, "reason": "Last response does not mention Alice"}
            with pytest.raises(AssertionError, match="does not reference"):
                conversation = [
                    {"role": "user", "content": "My name is Alice."},
                    {"role": "assistant", "content": "Hello! How can I assist you today?"},
                ]
                last_response_should_reference(conversation, "Alice")

    def test_fails_when_history_is_empty(self, mock_env):
        with pytest.raises(AssertionError, match="empty"):
            last_response_should_reference([], "anything")
