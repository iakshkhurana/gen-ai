from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone

load_dotenv()

client = OpenAI()

# Vector Embeddings generation

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="I am Cheetah"
)

print("Vector Embeddings : ", response)
print("Length = ", len(response.data[0].embedding))

# Add ON : Pinecone

pc = Pinecone()
index = pc.Index("idx")
index.upsert(vectors=[
    {"id":"node-1","values": response.data[0].embedding, "metadata":{"text":"Node.js is used to write backends."}}
])