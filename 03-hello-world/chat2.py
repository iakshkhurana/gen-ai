from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# Few-shot Prompting : The model is provided with a few examples before it to generate a response

SYSTEM_PROMPT = """
    You are an AI expert in Coding. You only know Python and nothing else. You help users in solving there python doubts only and nothing else. If user tried to ask something else apart from Python you can just roast them.
    
    Examples : 
    User : How to make a Tea?
    Assistant : Oh my love! It seems like you don't have a girlfriend.


    Examples : 
    User : How to write a function in python
    Assistant : def fn_name(x:int)-> int:
        pass # logic of the function
"""


response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role":"system", "content":SYSTEM_PROMPT},
        {"role": "user", "content": "Hello, my name is Aksh"},
        {"role": "assistant", "content": "Hi Aksh! How can I assist you today?"},
        {"role": "user", "content": "Why 75% attendance is imp of colleges"},
    ]
)

print(response.choices[0].message.content)