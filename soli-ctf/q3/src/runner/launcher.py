import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from worker.manager import start_container, stop_container

if __name__ == '__main__':
    result = start_container.delay("teamX", "juice", "bkimminich/juice-shop")
    info = result.get(timeout=400)
    print("Started:", info)

    stop = stop_container.delay(info["name"])
    print("Stopped:", stop.get(timeout=80))
