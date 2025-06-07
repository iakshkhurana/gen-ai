# OPEN AI API KEY

# from dotenv import load_dotenv
# from openai import OpenAI

# load_dotenv()

# client = OpenAI()

# text = "Dog chases chat"

# response = client.embeddings.create(
#    model = "text-embedding-3-small",
#    input = text
# )

# print(response)



# GEMINI API KEY

from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

text = "Dog chases chat"

response = genai.embed_content(
    model="models/embedding-001",
    content=text,
    task_type="retrieval_document"  # or "retrieval_query"
)

print(response['embedding'])