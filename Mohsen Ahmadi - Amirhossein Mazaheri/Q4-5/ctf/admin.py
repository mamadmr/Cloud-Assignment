from django.contrib import admin
from .models import Team, Challenge, ActiveContainer, ChallengeHistory

# Register all models so they appear in Django admin panel
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'docker_image', 'internal_port']

@admin.register(ActiveContainer)
class ActiveContainerAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'challenge', 'container_id', 'host_port', 'access_url', 'started_at']

@admin.register(ChallengeHistory)
class ChallengeHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'challenge', 'container_id', 'started_at', 'stopped_at']
