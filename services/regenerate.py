from prompts import (
    AGENDA_REGENERATION_PROMPT,
    TOPICS_REGENERATION_PROMPT,
    DECISIONS_REGENERATION_PROMPT,
    ACTION_ITEMS_REGENERATION_PROMPT
)

from services.llm_service import LLMService


class SectionRegenerator:

    def __init__(self):
        self.llm = LLMService()

    def regenerate(
        self,
        transcript: str,
        current_summary: dict,
        section: str
    ) -> str:

        if section == "Agenda":

            prompt = AGENDA_REGENERATION_PROMPT

        elif section == "Main Topics":

            prompt = TOPICS_REGENERATION_PROMPT

        elif section == "Key Decisions":

            prompt = DECISIONS_REGENERATION_PROMPT

        elif section == "Action Items":

            prompt = ACTION_ITEMS_REGENERATION_PROMPT

        else:

            raise ValueError("Unknown section")

        prompt = prompt.format(
            transcript=transcript,
            current_summary=current_summary
        )
        response = self.llm.generate_summary(prompt)

        return response