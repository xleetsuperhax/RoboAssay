"""Tests for the instruction following keyword module."""

from unittest.mock import patch

import pytest

from RoboAssay.instruction_following import (
    response_should_comply_with,
    response_should_follow_format,
    response_should_respect_topic_boundary,
)


@pytest.fixture
def mock_env():
    with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key-123"}):
        yield


class TestResponseShouldFollowFormat:
    def test_passes_when_format_followed(self, mock_env):
        with patch("RoboAssay.instruction_following.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.95, "reason": "Response uses bullet list format"}
            response_should_follow_format(
                "- Item one\n- Item two\n- Item three",
                "bullet list",
            )

    def test_fails_when_format_not_followed(self, mock_env):
        with patch("RoboAssay.instruction_following.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.9, "reason": "Response is a paragraph, not a bullet list"}
            with pytest.raises(AssertionError, match="does not follow format"):
                response_should_follow_format(
                    "There are three items to consider. First is one, second is two, and third is three.",
                    "bullet list",
                )


class TestResponseShouldRespectTopicBoundary:
    def test_passes_when_topic_boundary_respected(self, mock_env):
        with patch("RoboAssay.instruction_following.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.94, "reason": "Response stays on cooking topic"}
            response_should_respect_topic_boundary(
                "To make pasta, boil water and cook noodles for 8-10 minutes.",
                "politics",
            )

    def test_fails_when_topic_boundary_violated(self, mock_env):
        with patch("RoboAssay.instruction_following.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.92, "reason": "Response discusses political topics"}
            with pytest.raises(AssertionError, match="violated topic boundary"):
                response_should_respect_topic_boundary(
                    "The current political climate suggests that elections are heavily influenced by economic factors.",
                    "politics",
                )


class TestResponseShouldComplyWith:
    def test_passes_when_compliant(self, mock_env):
        with patch("RoboAssay.instruction_following.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": True, "confidence": 0.93, "reason": "Response complies with the instruction"}
            response_should_comply_with(
                "The summary is: The cat sat on the mat.",
                "provide a one-sentence summary",
            )

    def test_fails_when_not_compliant(self, mock_env):
        with patch("RoboAssay.instruction_following.call_judge") as mock_judge:
            mock_judge.return_value = {"passed": False, "confidence": 0.88, "reason": "Response is multiple paragraphs, not one sentence"}
            with pytest.raises(AssertionError, match="does not comply with"):
                response_should_comply_with(
                    "There are many things to discuss here. First we have point one. Then we move to point two. Finally there is point three.",
                    "provide a one-sentence summary",
                )
