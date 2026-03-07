"""Tests for the judge utility module."""

import json
from unittest.mock import patch, MagicMock

import pytest
import requests

from RoboAssay.utils.judge import call_judge, DEFAULT_JUDGE_MODEL


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}, clear=False):
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

    def test_uses_default_model(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            with patch.dict("os.environ", {}, clear=False):
                # Remove override if present
                import os
                os.environ.pop("ROBOASSAY_JUDGE_MODEL", None)
                call_judge("rubric", "response")
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert payload["model"] == DEFAULT_JUDGE_MODEL

    def test_model_overridable_via_env(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            with patch.dict("os.environ", {"ROBOASSAY_JUDGE_MODEL": "claude-haiku-4-5-20251001"}):
                call_judge("rubric", "response")
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert payload["model"] == "claude-haiku-4-5-20251001"

    def test_sends_correct_headers(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            call_judge("rubric", "response")
            call_args = mock_post.call_args
            headers = call_args[1]["headers"]
            assert headers["x-api-key"] == "test-key-123"
            assert headers["anthropic-version"] == "2023-06-01"

    def test_sends_request_with_timeout(self, mock_env, mock_judge_response):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.return_value = mock_judge_response()
            call_judge("rubric", "response")
            call_args = mock_post.call_args
            assert call_args[1]["timeout"] == 30

    def test_raises_runtime_error_on_timeout(self, mock_env):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            mock_post.side_effect = requests.Timeout()
            with pytest.raises(RuntimeError, match="timed out"):
                call_judge("rubric", "response")

    def test_raises_runtime_error_on_http_error(self, mock_env):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            error_response = MagicMock()
            error_response.status_code = 429
            error_response.text = "Too Many Requests"
            http_err = requests.HTTPError(response=error_response)
            mock_post.return_value.raise_for_status.side_effect = http_err
            with pytest.raises(RuntimeError, match="429"):
                call_judge("rubric", "response")

    def test_raises_runtime_error_on_non_json_response(self, mock_env):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            response = MagicMock()
            response.raise_for_status = MagicMock()
            response.json.return_value = {"content": [{"text": "not valid json {{{"}]}
            response.text = '{"content": [{"text": "not valid json {{{"}]}'
            mock_post.return_value = response
            with pytest.raises(RuntimeError, match="non-JSON"):
                call_judge("rubric", "response")

    def test_raises_runtime_error_on_missing_verdict_keys(self, mock_env):
        with patch("RoboAssay.utils.judge.requests.post") as mock_post:
            response = MagicMock()
            response.raise_for_status = MagicMock()
            response.json.return_value = {
                "content": [{"text": json.dumps({"passed": True})}]
            }
            mock_post.return_value = response
            with pytest.raises(RuntimeError, match="missing expected keys"):
                call_judge("rubric", "response")
