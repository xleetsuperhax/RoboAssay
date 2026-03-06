"""Tests for the judge utility module."""

import json
from unittest.mock import patch, MagicMock

import pytest

from RoboAssay.utils.judge import call_judge, JUDGE_MODEL


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


@pytest.fixture
def mock_judge_response():
    def _make_response(passed=True, confidence=0.95, reason="Test reason"):
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "content": [
                {
                    "text": json.dumps(
                        {
                            "passed": passed,
                            "confidence": confidence,
                            "reason": reason,
                        }
                    )
                }
            ]
        }
        response.raise_for_status = MagicMock()
        return response

    return _make_response


class TestCallJudge:
    def test_raises_without_api_key(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="ANTHROPIC_API_KEY"):
                call_judge("rubric", "response")

    def test_returns_passing_verdict(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response(passed=True)
            result = call_judge("test rubric", "test response")
            assert result["passed"] is True
            assert result["confidence"] == 0.95
            assert result["reason"] == "Test reason"

    def test_returns_failing_verdict(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response(
                passed=False, reason="Failed check"
            )
            result = call_judge("test rubric", "test response")
            assert result["passed"] is False
            assert result["reason"] == "Failed check"

    def test_includes_context_in_prompt(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            call_judge("rubric", "response", context="some context")
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            prompt = payload["messages"][0]["content"]
            assert "CONTEXT:" in prompt
            assert "some context" in prompt

    def test_excludes_context_when_empty(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            call_judge("rubric", "response")
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            prompt = payload["messages"][0]["content"]
            assert "CONTEXT:" not in prompt

    def test_uses_correct_model(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            call_judge("rubric", "response")
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert payload["model"] == JUDGE_MODEL

    def test_sends_correct_headers(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            call_judge("rubric", "response")
            call_args = mock_post.call_args
            headers = call_args[1]["headers"]
            assert headers["x-api-key"] == "test-key-123"
            assert headers["anthropic-version"] == "2023-06-01"
