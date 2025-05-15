from fastapi import FastAPI, HTTPException
import docker
import time

app = FastAPI()
client = docker.from_env()

def start_ctf_container(team_id: str, challenge_id: str) -> str:
    container_name = f"ctf_{team_id}_{challenge_id}"
    try:
        container = client.containers.run(
            image=f"ctf_challenge_{challenge_id}",  #the related image must be
            detach=True,
            name=container_name,
            labels={"team_id": team_id, "challenge_id": challenge_id}
        )
        time.sleep(1)
        container.reload()     
        ip_address = container.attrs['NetworkSettings']['IPAddress']
        return ip_address
    except docker.errors.APIError as e:
        raise Exception(f"Docker error: {e.explanation}")

def stop_ctf_container(team_id: str, challenge_id: str) -> bool:
    container_name = f"ctf_{team_id}_{challenge_id}"
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return True
    except docker.errors.NotFound:
        return False
    except docker.errors.APIError as e:
        raise Exception(f"Docker error: {e.explanation}")


# (i)(a) Assign a specific CTF container to a team based on team ID and challenge ID
# creating a new container
@app.post("/assign/")
def assign_container(team_id: str, challenge_id: str):
    try:
        ip_address = start_ctf_container(team_id, challenge_id)
	#(i)(c) the address of the container have to be in the response
	#return ip address to client to connect it
        return {"status": "success", "ip": ip_address}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# (i)(b) Remove a CTF container from a team using the team ID and the challenge ID
# Delete and stop endpoint of a container
@app.delete("/remove/")
def remove_container(team_id: str, challenge_id: str):
    try:
        success = stop_ctf_container(team_id, challenge_id)
        if success:
            return {"status": "removed"}
        else:
            raise HTTPException(status_code=404, detail="Container not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
