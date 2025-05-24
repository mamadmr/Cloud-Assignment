from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from auth_app.serializer import AddUserSerializer



class AddUser(ModelViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = AddUserSerializer
    http_method_names = ['post','get','put','patch']




    