import getpass
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = getpass.getpass("Enter your Groq API key: ")

llm = ChatGroq(model="llama-guard-3-8b", temperature=0, max_retries=2)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg)

# /Users/xava/calhacks/.venv/bin/python