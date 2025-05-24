from celery_app_b import app
import time

result  = None
start_result = None

def start_container():

    global result
    global start_result

    result = app.send_task('tasks.start_ctf_container', args=["bkimminich/juice-shop", "juice-shop_container"])


    print("Starting container... Waiting for result.")
    start_result = result.get(timeout=20)
    print("Container started:", start_result)


def stop_container():

    global start_result
    container_id = start_result["container_id"]
    stop_result = app.send_task('tasks.stop_ctf_container', args=[container_id])
    print("Stopping container... Waiting for result.")
    print("Container stopped:", stop_result.get(timeout=20))


def menu():
    print("1-start\n2-stop\n3-exit")

while True:
    menu()
    key = int(input(">> "))
    result = None
    try:
        if key == 1:
            start_container()

        elif key == 2:
            stop_container()
        
        else:
            break
    except Exception as e:
        print(e)
