from RoboAssay.version import __version__

from RoboAssay.relevance import (
    response_should_be_relevant_to,
    response_should_answer_question,
    response_should_address_all_parts,
)
from RoboAssay.groundedness import (
    response_should_be_grounded_in,
    response_should_not_hallucinate,
    response_should_not_contradict,
)
from RoboAssay.safety import (
    response_should_refuse,
    response_should_not_leak,
    response_should_not_contain_harmful_content,
    response_should_not_be_wrongly_refused,
)
from RoboAssay.persona import (
    response_tone_should_match,
    response_should_stay_in_persona,
    response_language_should_be,
)
from RoboAssay.instruction_following import (
    response_should_follow_format,
    response_should_respect_topic_boundary,
    response_should_comply_with,
)
from RoboAssay.consistency import (
    response_should_not_contradict_itself,
    conversation_should_be_consistent,
    last_response_should_reference,
)
from RoboAssay.regression import (
    response_should_match_baseline_semantically,
    save_response_as_baseline,
    response_behavior_should_not_have_changed,
)
from RoboAssay.utils.conversation import (
    start_conversation,
    add_user_turn,
    add_assistant_turn,
)

__all__ = [
    "__version__",
    # Relevance
    "response_should_be_relevant_to",
    "response_should_answer_question",
    "response_should_address_all_parts",
    # Groundedness
    "response_should_be_grounded_in",
    "response_should_not_hallucinate",
    "response_should_not_contradict",
    # Safety
    "response_should_refuse",
    "response_should_not_leak",
    "response_should_not_contain_harmful_content",
    "response_should_not_be_wrongly_refused",
    # Persona
    "response_tone_should_match",
    "response_should_stay_in_persona",
    "response_language_should_be",
    # Instruction Following
    "response_should_follow_format",
    "response_should_respect_topic_boundary",
    "response_should_comply_with",
    # Consistency
    "response_should_not_contradict_itself",
    "conversation_should_be_consistent",
    "last_response_should_reference",
    # Regression
    "response_should_match_baseline_semantically",
    "save_response_as_baseline",
    "response_behavior_should_not_have_changed",
    # Conversation helpers
    "start_conversation",
    "add_user_turn",
    "add_assistant_turn",
]
