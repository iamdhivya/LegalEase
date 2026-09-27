from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME


class GeminiDocumentGenerator:
    """
    Wraps the Gemini Interactions API. Builds a structured legal-document
    prompt from the four user-supplied fields and returns the generated text.
    """

    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is not set. Add it to your .env file "
                "(see .env.example)."
            )
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n"
            f"Ensure formal legal structure with multiple sections and legal clauses."
        )
        interaction = self.client.interactions.create(
            model=GEMINI_MODEL_NAME,
            input=prompt,
        )
        text = interaction.output_text
        if not text:
            raise ValueError(
                "Gemini returned an empty response. This can happen under "
                "high load — try generating again."
            )
        return text