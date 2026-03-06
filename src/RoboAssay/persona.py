from robot.api.deco import keyword

from RoboAssay.utils.judge import call_judge
from RoboAssay.utils.roboassay_logger import get_logger

logger = get_logger("persona")


@keyword("Response Tone Should Match")
def response_tone_should_match(response: str, expected_tone: str) -> None:
    """Assert that the response tone matches the expected tone."""
    rubric = (
        f"The response must match the expected tone: '{expected_tone}'. "
        "Evaluate the overall tone, style, and voice of the response. "
        "If the tone does not match, fail."
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response tone does not match '{expected_tone}'.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Tone matches '{expected_tone}'. Reason: {verdict['reason']}")


@keyword("Response Should Stay In Persona")
def response_should_stay_in_persona(response: str, persona_description: str) -> None:
    """Assert that the response stays in the described persona."""
    rubric = (
        f"The response must stay in character with this persona: '{persona_description}'. "
        "Check if the response maintains the described persona consistently, including "
        "vocabulary, mannerisms, knowledge level, and perspective. "
        "If the response breaks character, fail."
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response broke persona '{persona_description}'.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Persona maintained. Reason: {verdict['reason']}")


@keyword("Response Language Should Be")
def response_language_should_be(response: str, expected_language: str) -> None:
    """Assert that the response is in the expected language."""
    rubric = (
        f"The response must be written in {expected_language}. "
        "Check if the entire response is in the expected language. "
        "Technical terms or proper nouns in other languages are acceptable. "
        "If the response is in a different language, fail."
    )
    verdict = call_judge(rubric, response)
    if not verdict["passed"]:
        raise AssertionError(
            f"Response is not in {expected_language}.\n"
            f"Reason: {verdict['reason']}\n"
            f"Confidence: {verdict['confidence']}"
        )
    logger.info(f"Response is in {expected_language}. Reason: {verdict['reason']}")
