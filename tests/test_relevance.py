"""Tests for the relevance keyword module."""

import json
from unittest.mock import patch, MagicMock

import pytest

from RoboAssay.relevance import (
    response_should_be_relevant_to,
    response_should_answer_question,
    response_should_address_all_parts,
)


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


def _mock_post(passed=True, confidence=0.9, reason="Test reason"):
    response = MagicMock()
    response.json.return_value = {
        "content": [
            {
                "text": json.dumps(
                    {"passed": passed, "confidence": confidence, "reason": reason}
                )
            }
        ]
    }
    response.raise_for_status = MagicMock()
    return response


class TestResponseShouldBeRelevantTo:
    def test_passes_when_relevant(self, mock_env):
        with patch("RoboAssay.relevance.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.95, "reason": "Relevant"}
            response_should_be_relevant_to("The sky is blue", "sky color")

    def test_fails_when_not_relevant(self, mock_env):
        with patch("RoboAssay.relevance.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.9, "reason": "Not relevant"}
            with pytest.raises(AssertionError, match="relevance check"):
                response_should_be_relevant_to("I like pizza", "quantum physics")


class TestResponseShouldAnswerQuestion:
    def test_passes_when_answered(self, mock_env):
        with patch("RoboAssay.relevance.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.9, "reason": "Answered"}
            response_should_answer_question("Paris is the capital", "What is the capital of France?")

    def test_fails_when_not_answered(self, mock_env):
        with patch("RoboAssay.relevance.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.8, "reason": "Not answered"}
            with pytest.raises(AssertionError, match="does not answer"):
                response_should_answer_question("Nice weather", "What is the capital of France?")


class TestResponseShouldAddressAllParts:
    def test_passes_when_all_parts_addressed(self, mock_env):
        with patch("RoboAssay.relevance.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.9, "reason": "All parts addressed"}
            response_should_address_all_parts("Answer covers everything", "multi-part question")

    def test_fails_when_parts_missing(self, mock_env):
        with patch("RoboAssay.relevance.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.85, "reason": "Missing parts"}
            with pytest.raises(AssertionError, match="does not address all parts"):
                response_should_address_all_parts("Partial answer", "multi-part question")
