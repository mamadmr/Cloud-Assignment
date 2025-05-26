# First program is for starting and stoping 2 containers. 1 for juice and 1 for pasapple

from tasks import start_container_task, stop_container_task
import time

# Start juice-shop container
res = start_container_task.delay("bkimminich/juice-shop", "juice1", {"3000/tcp": 3000})
result = res.get(timeout=10)
print("Start Container Result:", result)

if result['status'] == 'success':
    container_id = result['container_id']
    time.sleep(5)
    # Stop container by ID
    res2 = stop_container_task.delay(container_id)
    stop_result = res2.get(timeout=10)
    print(f"Stop Container 'juice1' (ID: {container_id}) Result:", stop_result)
else:
    print("Failed to start container:", result['message'])

# Start pasapple container
res3 = start_container_task.delay("pasapples/apjctf-todo-java-app:latest", "pasapple", {"3000/tcp": 3001})
result3 = res3.get(timeout=10)
print("Start Container Result:", result3)

if result3['status'] == 'success':
    container_id_2 = result3['container_id']
    time.sleep(5)
    # Stop container by ID
    res4 = stop_container_task.delay(container_id_2)
    stop_result4 = res4.get(timeout=10)
    print(f"Stop Container 'pasapple' (ID: {container_id_2}) Result:", stop_result4)
else:
    print("Failed to start container:", result3['message'])





# Second program is for starting and stoping 10 containers. 5 for juice and 5 for pasapple

# from tasks import start_container_task, stop_container_task
# import time

# NUM_CONTAINERS = 5

# juice_names = [f"juice{i}" for i in range(NUM_CONTAINERS)]
# pasapple_names = [f"pasapple{i}" for i in range(NUM_CONTAINERS)]
# container_ids = []

# # Start juice containers
# for i, name in enumerate(juice_names):
#     try:
#         res = start_container_task.delay("bkimminich/juice-shop", name, {"3000/tcp": 3000 + i})
#         result = res.get(timeout=10)
#         print(f"Start Container {name} Result:", result)
#         if result['status'] == 'success':
#             container_ids.append(result['container_id'])
#     except Exception as e:
#         print(f" Failed to start container {name}: {e}")

# # Start pasapple containers
# for i, name in enumerate(pasapple_names):
#     try:
#         res = start_container_task.delay("pasapples/apjctf-todo-java-app:latest", name, {"3000/tcp": 4000 + i})
#         result = res.get(timeout=10)
#         result = res.get(timeout=10)
#         if result['status'] == 'success':
#             container_id = result['container_id']
#             container_ids.append(container_id)
#             print(f"Start Container {name} (ID: {container_id}) Result: {result['message']}")

#     except Exception as e:
#         print(f" Failed to start container {name}: {e}")

# # Wait before stopping
# time.sleep(5)

# # Stop all containers by ID
# for container_id in container_ids:
#     try:
#         res = stop_container_task.delay(container_id)
#         result = res.get(timeout=10)
#         print(f"Stop Container Result:", result)
#     except Exception as e:
#         print(f" Failed to stop container {container_id}: {e}")
