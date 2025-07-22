# Data ingestion
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

pdf_path = Path(__file__).parent / "all.pdf"

# Loading
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

print("Docs[0]",docs[0])

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 200
)

split_docs = text_splitter.split_documents(documents = docs)

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model = "text-embeddings-3-large"
)

# Using embedding model create embeddings of split_docs and store in db

vector_store = QdrantVectorStore.from_documents(
    documents = split_docs,
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

print("Indexing of Documents Done...")