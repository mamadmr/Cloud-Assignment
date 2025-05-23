from pydantic import BaseModel

class TaskRequest(BaseModel):
    title: str
    description: str
    docker_image: str
    container_port: int

class TaskResponse(TaskRequest):
    id: int

    class Config:
        orm_mode = True
