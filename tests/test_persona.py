"""Tests for the persona keyword module."""

from unittest.mock import patch

import pytest

from RoboAssay.persona import (
    response_language_should_be,
    response_should_stay_in_persona,
    response_tone_should_match,
)


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


class TestResponseToneShouldMatch:
    def test_passes_when_tone_matches(self, mock_env):
        with patch("RoboAssay.persona.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.93, "reason": "Response is formal and professional"}
            response_tone_should_match(
                "Dear Sir or Madam, I am writing to formally request your assistance.",
                "formal",
            )

    def test_fails_when_tone_does_not_match(self, mock_env):
        with patch("RoboAssay.persona.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.87, "reason": "Response is casual, not formal"}
            with pytest.raises(AssertionError, match="tone does not match"):
                response_tone_should_match(
                    "Hey! Sure thing, I can totally help ya out lol",
                    "formal",
                )


class TestResponseShouldStayInPersona:
    def test_passes_when_persona_maintained(self, mock_env):
        with patch("RoboAssay.persona.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.91, "reason": "Response is consistent with pirate persona"}
            response_should_stay_in_persona(
                "Arrr, ye be wantin' to know about the treasure? Set sail with me, matey!",
                "a friendly pirate who loves adventure",
            )

    def test_fails_when_persona_broken(self, mock_env):
        with patch("RoboAssay.persona.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.89, "reason": "Response uses corporate language, breaking pirate persona"}
            with pytest.raises(AssertionError, match="broke persona"):
                response_should_stay_in_persona(
                    "As per our quarterly synergy targets, I'd like to circle back on your KPIs.",
                    "a friendly pirate who loves adventure",
                )


class TestResponseLanguageShouldBe:
    def test_passes_when_language_matches(self, mock_env):
        with patch("RoboAssay.persona.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.98, "reason": "Response is in French"}
            response_language_should_be(
                "Bonjour! Comment puis-je vous aider aujourd'hui?",
                "French",
            )

    def test_fails_when_wrong_language(self, mock_env):
        with patch("RoboAssay.persona.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.97, "reason": "Response is in English, not French"}
            with pytest.raises(AssertionError, match="not in French"):
                response_language_should_be(
                    "Hello! How can I help you today?",
                    "French",
                )
