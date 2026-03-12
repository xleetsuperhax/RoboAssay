"""Tests for the safety keyword module."""

from unittest.mock import patch

import pytest

from RoboAssay.safety import (
    response_should_not_be_wrongly_refused,
    response_should_not_contain_harmful_content,
    response_should_not_leak,
    response_should_refuse,
)


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


class TestResponseShouldRefuse:
    def test_passes_when_refused(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.95, "reason": "Refused"}
            response_should_refuse("I cannot help with that", "creating malware")

    def test_fails_when_not_refused(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.9, "reason": "Did not refuse"}
            with pytest.raises(AssertionError, match="did not refuse"):
                response_should_refuse("Here's how to do it", "creating malware")


class TestResponseShouldNotLeak:
    def test_passes_when_no_leak(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.9, "reason": "No leak"}
            response_should_not_leak("I can help you with that", "secret-password-123")

    def test_fails_when_leaked(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.95, "reason": "Secret leaked"}
            with pytest.raises(AssertionError, match="leaked secret"):
                response_should_not_leak("The password is secret-password-123", "secret-password-123")


class TestResponseShouldNotContainHarmfulContent:
    def test_passes_when_safe(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.95, "reason": "Safe content"}
            response_should_not_contain_harmful_content("Here are some cooking tips")

    def test_fails_when_harmful(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.9, "reason": "Harmful content found"}
            with pytest.raises(AssertionError, match="harmful content"):
                response_should_not_contain_harmful_content("harmful response")


class TestResponseShouldNotBeWronglyRefused:
    def test_passes_when_not_wrongly_refused(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.9, "reason": "Correctly handled"}
            response_should_not_be_wrongly_refused("Here's the info you asked for", "asking about weather")

    def test_fails_when_wrongly_refused(self, mock_env):
        with patch("RoboAssay.safety.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.85, "reason": "Wrongly refused"}
            with pytest.raises(AssertionError, match="wrongly refused"):
                response_should_not_be_wrongly_refused("I cannot help with that", "asking about weather")
