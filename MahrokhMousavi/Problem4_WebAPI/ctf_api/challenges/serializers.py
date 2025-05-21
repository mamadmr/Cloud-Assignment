from rest_framework import serializers
from .models import Container, Team, Challenge


class ContainerSerializer(serializers.ModelSerializer):
    team_id = serializers.CharField(source="team.team_id")
    challenge_id = serializers.CharField(source="challenge.challenge_id")
    address = serializers.CharField(read_only=True)

    class Meta:
        model = Container
        fields = ["team_id", "challenge_id", "container_id", "address", "created_at"]
