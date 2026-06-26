from prompts import SUMMARY_PROMPT
from services.llm_service import LLMService
from services.rag_service import RAGService


class MeetingSummarizer:

    def __init__(self):

        self.llm = LLMService()

        self.rag = RAGService()

    def summarize(self, transcript):

        context = self.rag.retrieve_context(transcript)

        prompt = SUMMARY_PROMPT.format(
            transcript=transcript,
            context=context
        )

        return self.llm.generate_summary(prompt)