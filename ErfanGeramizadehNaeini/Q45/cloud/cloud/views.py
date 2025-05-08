from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from celery import Celery
from .models import Problem, Team, TeamProblem
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, inline_serializer
from rest_framework import serializers
app = Celery(
    'client',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)


class StartStopView(views.APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name='StartRequest',
            fields={
                'problem': serializers.IntegerField()
            }
        ),
        responses={
            200: inline_serializer(name='StartSuccess', fields={'status': serializers.CharField(), 'address': serializers.CharField()}),
            400: inline_serializer(name='StartFailure', fields={'error': serializers.CharField()})
        }
    )
    def post(self, request):
        problem = request.data.get("problem")
        if (not problem or not Problem.objects.filter(number=problem).exists()):
            return Response({"error": "problem not found"}, status=400)
        instance = TeamProblem.objects.filter(
            problem=problem, team=request.user).first()
        if not instance:
            instance = TeamProblem.objects.create(
                problem=Problem.objects.get(number=problem), team=request.user)
        elif instance.up:
            return Response({"error": "instance already up"}, status=400)
        setattr(instance, "up", True)
        all_ips = TeamProblem.objects.filter(
            up=True).order_by("ip").values_list('ip', flat=True)
        # index = 2
        # for ip in all_ips:
        #     if ip == f"{settings.HOST_PORTION}.{index}":
        #         break
        # if (index > 255):
        #     return Response({"error": "no ip available"}, status=400)
        # setattr(instance, "ip", f"{settings.HOST_PORTION}.{index}")

        all_ports = TeamProblem.objects.filter(
            up=True).order_by("port").values_list('port', flat=True)
        index = 2001
        for port in all_ports:
            if port != index:
                break
        setattr(instance, "port", f"{index}")

        instance.save()
        app.send_task('tasks.start', args=[instance.id])

        return Response({"status": "started", "address": request.get_host().split(":")[0]+":"+str(index)}, status=200)

    @extend_schema(
        request=inline_serializer(
            name='StopRequest',
            fields={
                'problem': serializers.IntegerField()
            }
        ),
        responses={
            200: inline_serializer(name='StopSuccess', fields={'status': serializers.CharField()}),
            400: inline_serializer(name='StopFailure', fields={'error': serializers.CharField()})
        }
    )
    def delete(self, request):
        problem = request.data.get("problem")
        if (not problem or not Problem.objects.filter(number=problem).exists()):
            return Response({"error": "problem not found"}, status=400)
        instance = TeamProblem.objects.filter(
            problem=problem, team=request.user).first()
        if not instance:
            return Response({"error": "instance is not up for this team"}, status=400)
        elif not instance.up:
            return Response({"error": "instance is not up"}, status=400)

        setattr(instance, "up", False)
        instance.save()

        app.send_task('tasks.stop', args=[instance.id])

        return Response({"status": "stoped"}, status=200)


# class GetIPView(views.APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         problem = request.data.get("problem")
#         if (not problem or not Problem.objects.filter(id=problem).exists()):
#             return Response({"error": "problem not found"}, status=400)
#         instance = TeamProblem.objects.filter(
#             problem=problem, team=request.user).first()
#         if not instance:
#             return Response({"error": "instance is not up for this team"}, status=400)
#         elif not instance.up:
#             return Response({"error": "instance is not up"}, status=400)

#         return Response({"ip": instance.ip}, status=200)


class TeamRegisterView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=inline_serializer(
            name='RegisterRequest',
            fields={
                'username': serializers.CharField(),
                'password': serializers.CharField()
            }
        ),
        responses={
            201: inline_serializer(name='RegisterSuccess', fields={'access': serializers.CharField(), 'refresh': serializers.CharField()}),
            400: OpenApiResponse(description='Error')
        }
    )
    def post(self, request):

        team_name = request.data.get('username')
        team_password = request.data.get('password')

        if not team_name or not team_password:
            return Response({'error': 'username and password is required'}, status=status.HTTP_400_BAD_REQUEST)
        if (Team.objects.filter(username=team_name).exists()):
            return Response({'error': 'Team with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user_model = get_user_model()
        team = user_model.objects.create_user(
            username=team_name, password=team_password
        )
        refresh = RefreshToken.for_user(team)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
