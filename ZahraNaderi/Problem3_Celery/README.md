## 1. Creating and Configuring the Celery App

In the `celery_app.py` file, a Celery application was defined using Redis as both the message broker and result backend. The `docker` module was also used to define tasks related to container management:

```python
app = Celery(
    'ctf_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)
```

### Defined Tasks:

**start\_container**
This task launches a new Docker container using the specified image. Optional port mappings and environment variables can also be passed:

```python
@app.task(name='start_container')
def start_container(image_name: str, ports: dict = None, env_vars: dict = None):
    ...
```

**stop\_container**
This task stops a Docker container using its `container_id`:

```python
@app.task(name='stop_container')
def stop_container(container_id: str):
    ...
```

All errors are handled gracefully using `try/except` blocks to ensure the program does not crash and instead returns a proper error message.

---

## 2. Running the Celery Worker

To start the Celery worker that processes the tasks, the following command was used:

```bash
celery -A celery_app worker --loglevel=info
```

The output confirmed a successful connection to Redis and the recognition of the defined tasks:

```
[tasks]
  . start_container
  . stop_container
```

---

## 3. Executing Tasks and Managing the Container Lifecycle

In the `test.py` file, the `start_container` task is called asynchronously. After a short delay (`sleep`), the status of the task is checked. If it succeeded, the `stop_container` task is triggered to stop the same container:

```python
result = start_container.delay(...)
...
if task.result.get("status") == "success":
    stop_result = stop_container.delay(...)
```

The script was executed with:

```bash
python test.py
```

And the output was as follows:

```
Task ID (Start): c83d8af6-a051-454a-adaa-1d46c1b8255e
State: SUCCESS
Result: {'status': 'success', 'container_id': '31f4c2c753b4688c391dde2b69b7ba04f02b214f41e5fe15b7575b024373d866'}

Task ID (Stop): 167069b2-9ee0-4961-b01a-46b3fbd61bfe
```

Video link:
[https://iutbox.iut.ac.ir/index.php/s/JjDqbNaNT9CJAs6](https://iutbox.iut.ac.ir/index.php/s/JjDqbNaNT9CJAs6)


