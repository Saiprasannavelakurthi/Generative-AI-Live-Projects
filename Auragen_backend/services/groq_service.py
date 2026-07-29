from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL_NAME
from utils.logger import logger


class GroqService:

    def __init__(self):

        self.llm = ChatGroq(
            model=MODEL_NAME,
            api_key=GROQ_API_KEY,
            temperature=0.2,
            max_tokens=2026
        )

    def generate(self, messages):

        try:
            response = self.llm.invoke(messages)
            return response.content

        except Exception as e:

            logger.exception("Groq generation failed")

            raise Exception(
                f"Groq API Error: {str(e)}"
            )

    def stream_generate(self, messages):

        try:

            for chunk in self.llm.stream(messages):

                if chunk.content:
                    yield chunk.content

        except Exception as e:

            logger.exception(
                "Groq streaming failed"
            )

            raise Exception(
                f"Groq Stream Error: {str(e)}"
            )


groq_service = GroqService()