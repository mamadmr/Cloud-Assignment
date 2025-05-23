from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Challenge, ActiveContainer
from .tasks import start_challenge_container, stop_challenge_container
from .serializers import TeamSerializer, ChallengeSerializer
from rest_framework import viewsets
from celery.result import AsyncResult
from django.conf import settings

class AssignChallenge(APIView):
    def post(self, request):
        team_id = request.data.get("team_id")
        challenge_id = request.data.get("challenge_id")

        try:
            team = Team.objects.get(id=team_id)
            challenge = Challenge.objects.get(id=challenge_id)
        except (Team.DoesNotExist, Challenge.DoesNotExist):
            return Response({"error": "Invalid team or challenge ID."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if an active container already exists for this team and challenge
        existing = ActiveContainer.objects.filter(team=team, challenge=challenge).first()
        if existing:
            return Response({
                "message": "Container already running for this team and challenge.",
                "container_id": existing.container_id,
                "access_url": existing.access_url
            }, status=status.HTTP_200_OK)

        # If no container is running, start one using Celery
        result = start_challenge_container.delay(team_id, challenge_id)

        return Response({
            "task_id": result.id,
            "status": "queued",
            "team_id": team.id,
            "team_name": team.name,
            "challenge_id": challenge.id,
            "challenge_name": challenge.name,
            "docker_image": challenge.docker_image,
            "expected_port": challenge.internal_port
        }, status=status.HTTP_202_ACCEPTED)

class RemoveChallenge(APIView):
    def post(self, request):
        team_id = request.data.get("team_id")
        challenge_id = request.data.get("challenge_id")

        result = stop_challenge_container.delay(team_id, challenge_id)

        return Response({
            "task_id": result.id,
            "status": "queued for removal",
            "team_id": team_id,
            "challenge_id": challenge_id
        }, status=status.HTTP_202_ACCEPTED)

class ActiveContainerInfo(APIView):
    def get(self, request):
        team_id = request.query_params.get("team_id")
        challenge_id = request.query_params.get("challenge_id")

        try:
            active = ActiveContainer.objects.get(team_id=team_id, challenge_id=challenge_id)
        except ActiveContainer.DoesNotExist:
            return Response({"error": "No active container found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "team_id": active.team.id,
            "team_name": active.team.name,
            "challenge_id": active.challenge.id,
            "challenge_name": active.challenge.name,
            "container_id": active.container_id,
            "host_port": active.host_port,
            "access_url": active.access_url,
            "started_at": active.started_at
        })
