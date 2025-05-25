from rest_framework import serializers
from django.contrib.auth.models import User

class AddUserSerializer(serializers.ModelSerializer):

    class Meta():
        model = User
        fields = ['username','password','is_active']