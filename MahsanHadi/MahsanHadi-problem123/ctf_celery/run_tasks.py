from celery_tasks import start_ctf_container, stop_ctf_container

# start a container for test
result1 = start_ctf_container.delay('nginx', 'my_nginx_ctf')

print("running...")
print(result1.get(timeout=10))

# stop a container for test
# result2 = stop_ctf_container.delay('my_nginx_ctf')
# print(result2.get(timeout=10))