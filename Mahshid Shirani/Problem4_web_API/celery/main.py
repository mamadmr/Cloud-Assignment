from tasks import start_ctf_container, stop_ctf_container

@app.post("/assign")
def assign_container(req: ChallengeRequest):
    task = start_ctf_container.delay(req.team_id, req.challenge_id)
    return {"message": "Container assignment task submitted", "task_id": task.id}

@app.delete("/remove")
def remove_container(req: ChallengeRequest):
    task = stop_ctf_container.delay(req.team_id, req.challenge_id)
    return {"message": "Container removal task submitted", "task_id": task.id}




from celery_worker import start_container_task

@app.post("/background/assign")
def background_assign(req: ChallengeRequest):
    start_container_task.delay(req.team_id, req.challenge_id)
    return {"message": "Container assignment task sent to background"}
