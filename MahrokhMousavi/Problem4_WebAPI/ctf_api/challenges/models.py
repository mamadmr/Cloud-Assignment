from django.db import models


class Team(models.Model):
    team_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    challenge_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    image = models.CharField(
        max_length=200
    )  # Docker image, e.g., pasapples/apjctf-todo-java-app:latest

    def __str__(self):
        return self.name


class Container(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    container_id = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=200)  # e.g., http://<container_ip>:<port>
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.team.name} - {self.challenge.name}"
