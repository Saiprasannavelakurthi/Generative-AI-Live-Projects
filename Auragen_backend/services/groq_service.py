from langchain_groq import ChatGroq
from config import GROQ_API_KEY, MODEL_NAME

class GroqService:

    def __init__(self):

        self.llm = ChatGroq(
            model=MODEL_NAME,
            api_key=GROQ_API_KEY,
            temperature=0.2,
            max_tokens=2026
        )

    def generate(self, prompt):
        try:
            response = self.llm.invoke(prompt)
            return response.content

        except Exception as e:
            raise Exception(f"Groq API Error: {str(e)}")


# Singleton instance
groq_service = GroqService()
