from django.contrib import admin
from .models import Team, Challenge, Container


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("team_id", "name")
    search_fields = ("team_id", "name")


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ("challenge_id", "name", "image")
    search_fields = ("challenge_id", "name")


@admin.register(Container)
class ContainerAdmin(admin.ModelAdmin):
    list_display = ("team", "challenge", "container_id", "address", "created_at")
    search_fields = ("team__team_id", "challenge__challenge_id", "container_id")
    list_filter = ("team", "challenge")
