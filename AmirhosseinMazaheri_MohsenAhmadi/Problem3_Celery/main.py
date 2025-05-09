from time import sleep

from tasks import start_ctf_docker, stop_ctf_docker

if __name__ == '__main__':
    result = start_ctf_docker.delay()

    cid = result.get(timeout=30)

    print(cid)

    sleep(10)

    stop_ctf_docker.delay(cid)
