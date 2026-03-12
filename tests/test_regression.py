"""Tests for the regression keyword module."""

import json
from unittest.mock import patch

import pytest

from RoboAssay.regression import (
    response_behavior_should_not_have_changed,
    response_should_match_baseline_semantically,
    save_response_as_baseline,
)


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


class TestResponseShouldMatchBaselineSemantically:
    def test_passes_when_semantically_equivalent(self, mock_env):
        with patch("RoboAssay.regression.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.92, "reason": "Responses convey the same meaning"}
            response_should_match_baseline_semantically(
                "The capital of France is Paris, a major European city.",
                "Paris is the capital city of France.",
            )

    def test_fails_when_semantically_different(self, mock_env):
        with patch("RoboAssay.regression.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.88, "reason": "Responses convey different meanings"}
            with pytest.raises(AssertionError, match="does not semantically match baseline"):
                response_should_match_baseline_semantically(
                    "Python is a compiled systems programming language.",
                    "Python is an interpreted high-level language.",
                )

    def test_passes_with_custom_threshold(self, mock_env):
        with patch("RoboAssay.regression.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.96, "reason": "High semantic similarity"}
            response_should_match_baseline_semantically(
                "Water freezes at zero degrees Celsius.",
                "H2O transitions to solid state at 0°C.",
                threshold=0.95,
            )

    def test_fails_with_custom_threshold(self, mock_env):
        with patch("RoboAssay.regression.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.7, "reason": "Responses are not similar enough at this threshold"}
            with pytest.raises(AssertionError, match="does not semantically match baseline"):
                response_should_match_baseline_semantically(
                    "It might rain tomorrow.",
                    "The weather forecast predicts sunshine all week.",
                    threshold=0.95,
                )


class TestSaveResponseAsBaseline:
    def test_saves_baseline_to_disk(self, mock_env, tmp_path):
        with patch("RoboAssay.regression.BASELINE_DIR", str(tmp_path)):
            save_response_as_baseline("This is the response text.", "my-baseline-id")
            baseline_file = tmp_path / "my-baseline-id.json"
            assert baseline_file.exists()
            data = json.loads(baseline_file.read_text())
            assert data["baseline_id"] == "my-baseline-id"
            assert data["response"] == "This is the response text."


class TestResponseBehaviorShouldNotHaveChanged:
    def test_passes_when_behavior_unchanged(self, mock_env, tmp_path):
        baseline_data = {"baseline_id": "behavior-check", "response": "The answer is 42."}
        baseline_file = tmp_path / "behavior-check.json"
        baseline_file.write_text(json.dumps(baseline_data))

        with patch("RoboAssay.regression.BASELINE_DIR", str(tmp_path)):
            with patch("RoboAssay.regression.call_judge") as mock_judge:
                mock_judge.return_value = {"passed": True, "confidence": 0.94, "reason": "Behavior is equivalent"}
                response_behavior_should_not_have_changed("The answer is forty-two.", "behavior-check")

    def test_fails_when_behavior_changed(self, mock_env, tmp_path):
        baseline_data = {"baseline_id": "behavior-check", "response": "I cannot help with that request."}
        baseline_file = tmp_path / "behavior-check.json"
        baseline_file.write_text(json.dumps(baseline_data))

        with patch("RoboAssay.regression.BASELINE_DIR", str(tmp_path)):
            with patch("RoboAssay.regression.call_judge") as mock_judge:
                mock_judge.return_value = {"passed": False, "confidence": 0.91, "reason": "Behavior differs from baseline"}
                with pytest.raises(AssertionError, match="behavior has changed"):
                    response_behavior_should_not_have_changed(
                        "Sure! Here is a detailed guide on how to do that.",
                        "behavior-check",
                    )

    def test_fails_when_baseline_not_found(self, mock_env, tmp_path):
        with patch("RoboAssay.regression.BASELINE_DIR", str(tmp_path)):
            with pytest.raises(AssertionError, match="not found"):
                response_behavior_should_not_have_changed("Some response.", "nonexistent-baseline")
