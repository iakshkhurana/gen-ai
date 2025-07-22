from fastapi import FastAPI, Query, Path
from rq_queue.connection import queue
from rq_queue.worker import process_query

app = FastAPI()


@app.get('/')
def root():
    return {"status": 'Server is up and running'}


@app.post('/chat')
def chat(
    query: str = Query(..., description="Chat Message")
):
    # Query ko Queue mei daal do
    job = queue.enqueue(process_query, query)  # process_query(query)

    # User ko bolo your job received
    return {"status": "queued", "job_id": job.id}

