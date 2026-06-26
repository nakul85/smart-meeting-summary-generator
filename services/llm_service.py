from google import genai
from google.genai.errors import ClientError

from config import GEMINI_API_KEY, MODEL_NAME


class LLMService:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_summary(self, prompt: str):

        try:

            response = self.client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text.replace("```json", "", 1)

            if text.startswith("```"):
                text = text.replace("```", "", 1)

            if text.endswith("```"):
                text = text[:-3]

            return text.strip()

        except ClientError as e:

            message = str(e)

            if "429" in message or "RESOURCE_EXHAUSTED" in message:

                raise Exception(
                    "Gemini API quota exceeded.\n\n"
                    "Please wait a minute and try again.\n\n"
                    "If the issue continues, generate a new Gemini API key "
                    "and update your .env file."
                )

            raise Exception(
                "Unable to connect to Gemini API.\n\n"
                "Please check your internet connection and API key."
            )