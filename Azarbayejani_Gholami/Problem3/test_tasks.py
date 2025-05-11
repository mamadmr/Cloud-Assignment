from tasks import start_container, stop_container

if __name__ == "__main__":
    # Start a container
    start_result = start_container.delay("pasapples/apjctf-todo-java-app:latest", "test_redis_ctf")
    cid = start_result.get(timeout=30)
    print("Started =>", cid)

    # Stop the same container
    stop_result = stop_container.delay("test_redis_ctf")
    print(stop_result.get(timeout=30))

    