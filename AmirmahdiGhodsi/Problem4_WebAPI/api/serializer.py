from rest_framework import serializers
from api.models import Container
from main_app.models import User

class ContainerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Container
        fields = ['user', 'image_name', 'container_name']


    def validate(self, data):
        user = User.objects.get(username=data['user'])
        data['container_name'] = data['container_name'] + '-ID-' + str(user.pk)
        return super().validate(data)

class ContainerControlSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta():
        model = Container
        fields = ['pk','user']