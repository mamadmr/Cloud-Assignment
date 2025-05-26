from task import start_container, stop_container

# Start a container
#result = start_container.delay('nginx', container_name='ctf_nginx')
#print(result.get(timeout=10))

# You can also retrieve container list with Docker CLI:
# docker ps -a

#Stop the container (use the container ID from the output above)
stop_container.delay('ctf_nginx')
