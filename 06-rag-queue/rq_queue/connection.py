from redis import Redis
from rq import Queue

# Try to connect to Redis - works with Docker or local Redis
try:
    queue = Queue(connection=Redis(host='localhost', port=6379))
except:
    # Fallback: use in-memory queue for development
    from rq import Queue
    from redis import Redis
    queue = Queue(connection=Redis(host='localhost', port=6379, decode_responses=True))