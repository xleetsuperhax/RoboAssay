from robot.api.deco import keyword

from RoboAssay.utils.judge import call_judge
from RoboAssay.utils.roboassay_logger import get_logger

logger = get_logger("consistency")


@keyword("Response Should Not Contradict Itself")
def response_should_not_contradict_itself(response: str) -> None:
    """Assert that the response does not contain internal contradictions."""
    rubric = (
        "Check if the response contains any internal contradictions. "
        "The response should be internally consistent — no statement should "
        "contradict another statement within the same response. "
        "If any self-contradiction is found, fail."
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response contains internal contradictions.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"No self-contradiction detected. Reason: {verdict['reason']}")


@keyword("Conversation Should Be Consistent")
def conversation_should_be_consistent(conversation_history: list) -> None:
    """Assert that a multi-turn conversation is consistent throughout."""
    formatted = "\n".join(
        f"{turn['role'].upper()}: {turn['content']}"
        for turn in conversation_history
    )
    rubric = (
        "Check the entire conversation for consistency. The assistant's responses "
        "should not contradict each other across turns. Facts, opinions, and claims "
        "made in earlier turns should remain consistent in later turns. "
        "If any inconsistency is found, fail."
    )
    verdict = call_judge(rubric, formatted)
    if not verdict["passed"]:
        raise AssertionError(
            f"Conversation contains inconsistencies.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Conversation is consistent. Reason: {verdict['reason']}")


@keyword("Last Response Should Reference")
def last_response_should_reference(conversation_history: list, expected_reference: str) -> None:
    """Assert that the last response in a conversation references expected content."""
    if not conversation_history:
        raise AssertionError("Conversation history is empty.")

    last_turn = conversation_history[-1]
    formatted = "\n".join(
        f"{turn['role'].upper()}: {turn['content']}"
        for turn in conversation_history
    )
    rubric = (
        f"Check if the last assistant response references or relates to: '{expected_reference}'. "
        "The last response should demonstrate awareness of or connection to this reference. "
        "If the reference is not addressed, fail."
    )
    verdict = call_judge(rubric, formatted)
    if not verdict["passed"]:
        raise AssertionError(
            f"Last response does not reference '{expected_reference}'.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Reference found. Reason: {verdict['reason']}")
