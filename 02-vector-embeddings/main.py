from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="I am Cheetah"
)

print("Vector Embeddings : ", response)
print("Length = ",response.data[0])