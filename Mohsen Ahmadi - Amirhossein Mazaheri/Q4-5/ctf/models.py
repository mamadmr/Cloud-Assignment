from django.utils import timezone
from django.db import models

# Team model represents a participating CTF team
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Challenge model holds Docker image and info about a CTF challenge
class Challenge(models.Model):
    name = models.CharField(max_length=100)
    docker_image = models.CharField(max_length=200)
    internal_port = models.IntegerField(default=80)  # Default port inside the container

    def __str__(self):
        return self.name

# ActiveContainer keeps track of running Docker containers for each team/challenge
class ActiveContainer(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    container_id = models.CharField(max_length=100)
    host_port = models.IntegerField()
    access_url = models.URLField()
    started_at = models.DateTimeField(auto_now_add=True)

# ChallengeHistory logs all start/stop events for auditing
class ChallengeHistory(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    container_id = models.CharField(max_length=255, unique=True)
    started_at = models.DateTimeField(default=timezone.now)
    stopped_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.team} - {self.challenge} ({self.container_id})"