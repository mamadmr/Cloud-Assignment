from rest_framework import serializers
from account_app.models import Container
from auth_app.models import User

class ContainerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    port = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Container
        fields = ['user', 'image_name', 'container_name', 'port']


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