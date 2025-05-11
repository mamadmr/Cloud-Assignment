# test_task.py

from task import start_ctf_container

result = start_ctf_container.delay("alpine")  # or any test image you have
print(result.get(timeout=10))  # This now works since a result backend is set
