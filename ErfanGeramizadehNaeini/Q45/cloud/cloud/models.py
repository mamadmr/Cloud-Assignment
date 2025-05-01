from django.db import models
from django.contrib.auth.models import AbstractUser


class Team(AbstractUser):
    problem1_up = models.BooleanField(default=False)
    peoblem2_up = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Problem(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_name = models.CharField(max_length=100)
    port = models.IntegerField()

    def __str__(self):
        return self.name


class TeamProblem(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    up = models.BooleanField(default=False)
    ip = models.CharField(max_length=100, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    container_id = models.CharField(max_length=100, null=True, blank=True)
