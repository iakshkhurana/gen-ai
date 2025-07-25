from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

text = "Dog chases chat"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

print(response)
