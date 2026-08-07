import time

from langchain_groq import ChatGroq

from config import GROQ_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS
from utils.logger import logger


class GroqService:
    """
    Handles communication with the Groq LLM.
    """

    def __init__(self):
        self.llm = ChatGroq(
            model=MODEL_NAME,
            api_key=GROQ_API_KEY,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

    def generate(self, messages: list) -> str:
        """
        Generate a complete React component.
        """

        if not messages:
            raise ValueError("Messages cannot be empty.")

        start_time = time.perf_counter()

        try:
            response = self.llm.invoke(messages)

            if response is None or not hasattr(response, "content"):
                raise RuntimeError("Empty response received from Groq.")

            content = response.content.strip()

            elapsed = round(time.perf_counter() - start_time, 2)

            logger.info(
                f"Groq generation completed in {elapsed}s."
            )

            print("\n========== GROQ RESPONSE ==========")
            print(content)
            print("===================================\n")

            return content

        except Exception as e:
            logger.exception("Groq generation failed.")

            raise RuntimeError(
                f"Groq API Error: {e}"
            ) from e

    def stream_generate(self, messages: list):
        """
        Stream React component tokens from Groq.
        """

        if not messages:
            raise ValueError("Messages cannot be empty.")

        start_time = time.perf_counter()

        try:
            full_response = ""

            for chunk in self.llm.stream(messages):

                if not chunk:
                    continue

                token = getattr(chunk, "content", "")

                if not token:
                    continue

                full_response += token

                yield token

            elapsed = round(
                time.perf_counter() - start_time,
                2,
            )

            logger.info(
                f"Groq streaming completed in {elapsed}s."
            )

            print("\n========== GROQ STREAM OUTPUT ==========")
            print(full_response)
            print("========================================\n")

        except Exception as e:
            logger.exception("Groq streaming failed.")

            raise RuntimeError(
                f"Groq Stream Error: {e}"
            ) from e


groq_service = GroqService()