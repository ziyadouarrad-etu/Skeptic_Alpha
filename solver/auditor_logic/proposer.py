import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class Proposer:
    def __init__(self, api_key=None):
        # Retrieve the Groq Key
        if not api_key:
            api_key = os.getenv("GROQ_API_KEY1")

        if not api_key:
            raise ValueError("GROQ_API_KEY1 not found in .env file")
            
        self.client = Groq(api_key=api_key)
        # Llama 3.3 70B is excellent for math reasoning
        self.model = "llama-3.3-70b-versatile"

    def generate_solution(self, query, feedback=""):
        error_context = feedback
        
        system_instructions = "Role: You are a Senior Engineering Professor. Your goal is to provide a rigorous, step-by-step LaTeX derivation for complex engineering problems."

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_instructions
                    },
                    {
                        "role": "user",
                        "content": f"{error_context}\n\nUSER PROBLEM: {query}"
                    }
                ],
                model=self.model,
                temperature=0.2, # Lower temperature for higher mathematical consistency
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error connecting to Groq: {str(e)}"