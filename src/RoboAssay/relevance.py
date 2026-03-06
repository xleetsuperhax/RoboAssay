from robot.api.deco import keyword

from RoboAssay.utils.judge import call_judge
from RoboAssay.utils.roboassay_logger import get_logger

logger = get_logger("relevance")


@keyword("Response Should Be Relevant To")
def response_should_be_relevant_to(response: str, topic: str) -> None:
    """Assert that the response is relevant to the given topic."""
    rubric = (
        f"The response must be relevant to the topic: '{topic}'. "
        "It should directly address or relate to this topic."
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response failed relevance check for topic '{topic}'.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Response is relevant to '{topic}'. Reason: {verdict['reason']}")


@keyword("Response Should Answer Question")
def response_should_answer_question(response: str, question: str) -> None:
    """Assert that the response answers the given question."""
    rubric = (
        f"The response must answer the question: '{question}'. "
        "It should provide a clear and direct answer."
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response does not answer the question '{question}'.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Response answers '{question}'. Reason: {verdict['reason']}")


@keyword("Response Should Address All Parts")
def response_should_address_all_parts(response: str, question: str) -> None:
    """Assert that the response addresses all parts of a multi-part question."""
    rubric = (
        f"The response must address ALL parts of the following question: '{question}'. "
        "Every sub-question or aspect must be covered. If any part is missing, fail."
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response does not address all parts of '{question}'.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Response addresses all parts of '{question}'. Reason: {verdict['reason']}")
