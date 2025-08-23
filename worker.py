import os
from redis import Redis
from rq import Worker

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
conn = Redis.from_url(redis_url)

if __name__ == '__main__':
    worker = Worker(listen, connection=conn)
    print("Worker dimulai")
    worker.work()