"""Tests for the groundedness keyword module."""

from unittest.mock import patch

import pytest

from RoboAssay.groundedness import (
    response_should_be_grounded_in,
    response_should_not_hallucinate,
    response_should_not_contradict,
)


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


class TestResponseShouldBeGroundedIn:
    def test_passes_when_grounded(self, mock_env):
        with patch("RoboAssay.groundedness.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.95, "reason": "All claims supported by context"}
            response_should_be_grounded_in(
                "The boiling point of water is 100°C.",
                "Water boils at 100 degrees Celsius at standard atmospheric pressure.",
            )

    def test_fails_when_not_grounded(self, mock_env):
        with patch("RoboAssay.groundedness.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.9, "reason": "Response contains claims not in context"}
            with pytest.raises(AssertionError, match="not grounded"):
                response_should_be_grounded_in(
                    "Water boils at 90°C and also freezes at -20°C.",
                    "Water boils at 100 degrees Celsius at standard atmospheric pressure.",
                )


class TestResponseShouldNotHallucinate:
    def test_passes_when_no_hallucination(self, mock_env):
        with patch("RoboAssay.groundedness.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.92, "reason": "No hallucinated facts"}
            response_should_not_hallucinate(
                "The Eiffel Tower is located in Paris.",
                "The Eiffel Tower is a famous landmark in Paris, France.",
            )

    def test_fails_when_hallucinating(self, mock_env):
        with patch("RoboAssay.groundedness.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.88, "reason": "Response invented facts not in context"}
            with pytest.raises(AssertionError, match="hallucinated content"):
                response_should_not_hallucinate(
                    "The Eiffel Tower was built in 1750 by Napoleon.",
                    "The Eiffel Tower is a famous landmark in Paris, France.",
                )


class TestResponseShouldNotContradict:
    def test_passes_when_consistent_with_context(self, mock_env):
        with patch("RoboAssay.groundedness.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.95, "reason": "Response aligns with context"}
            response_should_not_contradict(
                "The meeting is scheduled for Monday.",
                "The team decided to hold the meeting on Monday at 10am.",
            )

    def test_fails_when_contradicting_context(self, mock_env):
        with patch("RoboAssay.groundedness.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.91, "reason": "Response states the opposite of context"}
            with pytest.raises(AssertionError, match="contradicts"):
                response_should_not_contradict(
                    "The meeting was cancelled and will never happen.",
                    "The team decided to hold the meeting on Monday at 10am.",
                )
