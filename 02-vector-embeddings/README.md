# Vector Embeddings & Pinecone

## What are vector embeddings?

Vector embeddings are numerical representations of text (or images, audio, etc.) in high-dimensional space. Instead of treating words as strings, we convert them into arrays of floating-point numbers — typically 1536 dimensions for OpenAI's `text-embedding-3-small` model.

The key idea: **texts with similar meaning land close together in vector space.** So "I love dogs" and "I adore puppies" would have vectors that are nearly identical, even though the words are completely different.

## How the code works

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="I am Cheetah"
)
```

This sends the text `"I am Cheetah"` to OpenAI's embedding model and returns a vector of **1536 floats**. That vector is the mathematical meaning of the sentence.

`response.data[0].embedding` → the actual list of 1536 numbers like `[0.0023, -0.0091, 0.0412, ...]`

## Why do we need Pinecone?

Generating embeddings is only step one. You need somewhere to **store and search** them. That's what Pinecone does — it's a vector database.

Without Pinecone (or a similar DB), you'd have to:
- Store all vectors in memory or a flat file
- Loop through every single vector to find similar ones
- Handle scaling yourself

Pinecone gives you **fast approximate nearest neighbor (ANN) search** out of the box.

## Pinecone basics

### Index
A container for your vectors. You create one per project and set the dimension (must match your embedding model — 1536 for `text-embedding-3-small`).

### Upsert
Insert or update vectors. Each vector needs:

| Field | Description |
|-------|-------------|
| `id` | Unique identifier (e.g. `"node-1"`) |
| `values` | The embedding array (1536 floats) |
| `metadata` | Optional key-value pairs for filtering |

```python
index.upsert(vectors=[
    {
        "id": "node-1",
        "values": response.data[0].embedding,
        "metadata": {"text": "Node.js is used to write backends."}
    }
])
```

### Query
Find the most similar vectors to a given vector:

```python
results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
```

`top_k=3` means return the 3 closest matches.

## Similarity metrics

| Metric | Best for |
|--------|----------|
| Cosine | Text similarity (default, most common) |
| Euclidean | When magnitude matters |
| Dot product | When vectors are normalized |

## Important things to remember

- **Dimension must match** — if your model outputs 1536, your Pinecone index must be created with dimension 1536.
- **Metadata is for filtering** — store the original text, category, source, etc. so you can filter results during queries.
- **Embeddings are model-specific** — vectors from `text-embedding-3-small` can't be compared with vectors from a different model. Stick to one model per index.
- **Upsert = insert + update** — if you upsert with an existing `id`, it overwrites the old vector.

## The big picture (RAG pipeline)

```
User query
    ↓
Generate embedding (OpenAI)
    ↓
Search Pinecone (find similar vectors)
    ↓
Retrieve matching text from metadata
    ↓
Send text + query to LLM as context
    ↓
LLM generates an informed answer
```

This is called **Retrieval-Augmented Generation (RAG)** — the most common use case for vector embeddings + Pinecone.