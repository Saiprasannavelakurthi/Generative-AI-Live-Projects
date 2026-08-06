import time

from langchain_groq import ChatGroq

from config import GROQ_API_KEY, MODEL_NAME
from utils.logger import logger


class GroqService:

    def __init__(self):

        self.llm = ChatGroq(
            model=MODEL_NAME,
            api_key=GROQ_API_KEY,
            temperature=0.2,
            max_tokens=2048,
        )

    def generate(self, messages: list) -> str:

        if not messages:
            raise ValueError("Messages cannot be empty.")

        start_time = time.perf_counter()

        try:

            response = self.llm.invoke(messages)

            elapsed = round(
                time.perf_counter() - start_time,
                2,
            )

            logger.info(
                f"Groq response generated in {elapsed} sec."
            )

            # Print complete response for debugging
            print("\n========== GROQ RESPONSE ==========")
            print(response.content)
            print("===================================\n")

            return response.content

        except Exception as e:

            logger.exception(
                "Groq generation failed."
            )

            raise RuntimeError(
                f"Groq API Error: {str(e)}"
            )

    def stream_generate(self, messages: list):

        if not messages:
            raise ValueError("Messages cannot be empty.")

        start_time = time.perf_counter()

        try:

            full_response = ""

            for chunk in self.llm.stream(messages):

                if chunk.content:
                    full_response += chunk.content
                    yield chunk.content

            elapsed = round(
                time.perf_counter() - start_time,
                2,
            )

            logger.info(
                f"Groq streaming completed in {elapsed} sec."
            )

            # Print the final streamed response
            print("\n========== GROQ STREAM OUTPUT ==========")
            print(full_response)
            print("========================================\n")

        except Exception as e:

            logger.exception(
                "Groq streaming failed."
            )

            raise RuntimeError(
                f"Groq Stream Error: {str(e)}"
            )


groq_service = GroqService()