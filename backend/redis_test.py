# from rq import Worker, Queue, Connection, SimpleWorker
# from redis import Redis

# # Connect to Redis server
# redis_conn = Redis()

# # Specify which queues to listen to
# listen = ['default']

# if __name__ == '__main__':
#     with Connection(redis_conn):
#         worker = SimpleWorker(map(Queue, listen))
#         worker.work()
from celery import shared_task
from celery import Celery

from tasks import test_task

def main():
    # Run the test task
    result = test_task.apply_async().get(timeout=30)
    print(result)

if __name__ == '__main__':
    main()