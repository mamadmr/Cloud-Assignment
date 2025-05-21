from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
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
            task = start_container_task.delay(team.id, challenge.id)
            return Response(
                {"task_id": task.id, "message": "Container assignment in progress"},
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
            stop_container_task.delay(container.id)
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
