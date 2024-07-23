from celery import Celery

app = Celery('test', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

@app.task
def test_task():
    return 'Test Task Executed Successfully'

if __name__ == '__main__':
    result = test_task.apply_async()
    try:
        print(result.get(timeout = 10))
    except Exception as e:
        print(f"Error: {e}")
