from rest_framework import serializers
from .models import Team, Challenge, ActiveContainer

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = '__all__'

class ActiveContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveContainer
        fields = '__all__'

