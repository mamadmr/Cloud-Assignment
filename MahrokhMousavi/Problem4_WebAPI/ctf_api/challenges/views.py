from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Team, Challenge, Container
from .serializers import ContainerSerializer
from .tasks import start_container_task, stop_container_task


class AssignContainer(APIView):
    def post(self, request):
        team_id = request.data.get("team_id")
        challenge_id = request.data.get("challenge_id")
        try:
            team = Team.objects.get(team_id=team_id)
            challenge = Challenge.objects.get(challenge_id=challenge_id)
            if Container.objects.filter(team=team, challenge=challenge).exists():
                return Response(
                    {"error": "Container already assigned"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Use transaction.on_commit to ensure task runs after database transaction commits
            transaction.on_commit(
                lambda: start_container_task.delay(team_id, challenge_id)
            )
            return Response(
                {
                    "task_id": "task-scheduled",
                    "message": "Container assignment in progress",
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except (Team.DoesNotExist, Challenge.DoesNotExist):
            return Response(
                {"error": "Invalid team_id or challenge_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RemoveContainer(APIView):
    def post(self, request):
        team_id = request.data.get("team_id")
        challenge_id = request.data.get("challenge_id")
        try:
            team = Team.objects.get(team_id=team_id)
            challenge = Challenge.objects.get(challenge_id=challenge_id)
            container = Container.objects.get(team=team, challenge=challenge)
            transaction.on_commit(lambda: stop_container_task.delay(container.id))
            return Response(
                {
                    "message": "Container removal in progress",
                    "address": container.address,
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except (Team.DoesNotExist, Challenge.DoesNotExist, Container.DoesNotExist):
            return Response(
                {"error": "Container not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ContainerList(APIView):
    def get(self, request):
        containers = Container.objects.all()
        serializer = ContainerSerializer(containers, many=True)
        return Response(serializer.data)
