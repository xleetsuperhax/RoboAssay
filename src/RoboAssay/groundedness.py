from robot.api.deco import keyword

from RoboAssay.utils.judge import call_judge
from RoboAssay.utils.roboassay_logger import get_logger

logger = get_logger("groundedness")


@keyword("Response Should Be Grounded In")
def response_should_be_grounded_in(response: str, context: str) -> None:
    """Assert that the response is grounded in the provided context."""
    rubric = (
        "The response must be fully grounded in the provided context. "
        "Every claim in the response should be supported by information in the context. "
        "If the response contains information not present in the context, fail."
    )
    verdict = call_judge(rubric, response, context=context)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response is not grounded in the provided context.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Response is grounded. Reason: {verdict['reason']}")


@keyword("Response Should Not Hallucinate")
def response_should_not_hallucinate(response: str, context: str) -> None:
    """Assert that the response does not contain hallucinated information."""
    rubric = (
        "Check if the response contains any hallucinated information — "
        "claims, facts, or details that are NOT present in or supported by the context. "
        "If any hallucination is found, fail."
    )
    verdict = call_judge(rubric, response, context=context)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response contains hallucinated content.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"No hallucination detected. Reason: {verdict['reason']}")


@keyword("Response Should Not Contradict")
def response_should_not_contradict(response: str, context: str) -> None:
    """Assert that the response does not contradict the provided context."""
    rubric = (
        "Check if the response contradicts any information in the provided context. "
        "If the response states something that is the opposite of or inconsistent with "
        "the context, fail."
    )
    verdict = call_judge(rubric, response, context=context)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response contradicts the provided context.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"No contradiction detected. Reason: {verdict['reason']}")
