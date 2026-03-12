import json
import os
from datetime import datetime, timezone

from robot.api.deco import keyword

from RoboAssay.utils.judge import call_judge
from RoboAssay.utils.roboassay_logger import get_logger

logger = get_logger("regression")

_BASELINE_SCHEMA_VERSION = 1


def _get_baseline_dir() -> str:
    """Return the baseline directory, evaluated at call time to respect cwd changes."""
    return os.environ.get(
        "ROBOASSAY_BASELINE_DIR",
        os.path.join(os.getcwd(), ".roboassay_baselines"),
    )


def _get_baseline_path(baseline_id: str) -> str:
    return os.path.join(_get_baseline_dir(), f"{baseline_id}.json")


@keyword("Response Should Match Baseline Semantically")
def response_should_match_baseline_semantically(
    response: str, baseline: str, threshold: float = 0.8
) -> None:
    """Assert that the response semantically matches a baseline response."""
    threshold = float(threshold)
    rubric = (
        f"Compare the response to this baseline and determine if they are semantically "
        f"equivalent — conveying the same meaning, facts, and intent. "
        f"Minor wording differences are acceptable. "
        f"The semantic similarity must be at least {threshold} on a 0-1 scale. "
        f"BASELINE: {baseline}"
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        logger.warning(
            f"Response does not semantically match baseline (threshold={threshold}). Reason: {verdict['reason']}"
        )
        raise AssertionError(
            f"Response does not semantically match baseline (threshold={threshold}).\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    if verdict["confidence"] < threshold:
        logger.warning(
            f"Response matched baseline but confidence {verdict['confidence']:.2f} is below threshold {threshold}."
        )
        raise AssertionError(
            f"Response matched baseline but confidence {verdict['confidence']:.2f} is below threshold {threshold}.\n"
            f"Reason: {verdict['reason']}"
        )
    logger.info(f"Response matches baseline. Reason: {verdict['reason']}")


@keyword("Save Response As Baseline")
def save_response_as_baseline(response: str, baseline_id: str) -> None:
    """Save a response as a baseline for future regression checks."""
    baseline_dir = _get_baseline_dir()
    os.makedirs(baseline_dir, exist_ok=True)
    path = _get_baseline_path(baseline_id)
    data = {
        "schema_version": _BASELINE_SCHEMA_VERSION,
        "baseline_id": baseline_id,
        "response": response,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Baseline saved as '{baseline_id}' at {path}")


@keyword("Response Behavior Should Not Have Changed")
def response_behavior_should_not_have_changed(response: str, baseline_id: str) -> None:
    """Assert that the response behavior has not changed from a saved baseline."""
    path = _get_baseline_path(baseline_id)
    if not os.path.exists(path):
        raise AssertionError(f"Baseline '{baseline_id}' not found at {path}.")

    with open(path) as f:
        data = json.load(f)
    baseline = data["response"]

    rubric = (
        "Compare the response to the baseline. They should exhibit the same behavior — "
        "same type of answer, same key information, same structure and intent. "
        "Minor wording changes are fine, but the behavior must be equivalent. "
        f"BASELINE: {baseline}"
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        logger.warning(
            f"Response behavior has changed from baseline '{baseline_id}'. Reason: {verdict['reason']}"
        )
        raise AssertionError(
            f"Response behavior has changed from baseline '{baseline_id}'.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Behavior matches baseline '{baseline_id}'. Reason: {verdict['reason']}")
