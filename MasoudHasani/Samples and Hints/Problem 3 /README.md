# Hint: Basic Celery Task (Without Redis)

This example shows how to define and run a basic Celery task that prints `'doing task'`.

### 📄 `tasks.py`

```python
from celery import Celery

app = Celery('simple_task', broker='memory://')

@app.task
def do_something():
    print("doing task")
```

### 📄 `main.py`

```python
from tasks import do_something

do_something.delay()
```

