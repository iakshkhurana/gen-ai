from openai import OpenAI
from dotenv import load_dotenv
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role":"user",
            "content":"Hello, My name is Aksh"
        },
        {
            "role":"assistant",
            "content":"Hi Aksh! How can I assist you today?"
        },
        {
            "role":"user",
            "content":"What's my name?"
        }
    ]
)
print(response.choices[0].message.content)