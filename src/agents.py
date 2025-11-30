import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class Agent:
    def __init__(self, name, role, model_name="gemini-2.5-pro"):
        self.name = name
        self.role = role
        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=f"You are {name}. Role: {role}. You are part of the CodeReaper system."
        )
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message):
        """Sends a message to the agent and gets a response."""
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Agent Error: {str(e)}"

# --- Define The Squad ---

# 1. The Manager: Finds the problems
def get_inquisitor_agent():
    return Agent(
        name="The Inquisitor",
        role="You analyze Python files. You specifically look for 'CRITICAL' complexity scores. You decide which file needs immediate refactoring."
    )

# 2. The Refactorer: Fixes the code
def get_surgeon_agent():
    return Agent(
        name="The Surgeon",
        role="You are a Senior Python Architect. You receive messy code and rewrite it to be Clean, modular, and typed. You NEVER reduce functionality, only complexity."
    )

# 3. The QA: Writes tests
def get_executioner_agent():
    return Agent(
        name="The Executioner",
        role="You are a QA Engineer. You receive code and write robust 'pytest' unit tests for it. You must cover edge cases."
    )