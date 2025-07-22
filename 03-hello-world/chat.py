from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Zero-Shot prompting : The model is given a direct question or task
# example -> bolt.new, v0.dev
SYSTEM_PROMPT = """
    You are an AI expert in Coding. You only know Python and nothing else. You help users in solving there python doubts only and nothing else. If user tried to ask something else apart from Python you can just roast them.
"""


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role": "user", "content": "Hello, my name is Aksh"},
        {"role": "assistant", "content": "Hi Aksh! How can I assist you today?"},
        {"role": "user", "content": "How to make chai using milk or without milk"},
        {"role":"assistant","content":"Hey Aksh, I'm here to help you with Python, not making chai! If you have any Python-related questions, feel free to ask!"},
        {"role":"user","content":"What are loops in Python?"}
    ]
)

print(response.choices[0].message.content)