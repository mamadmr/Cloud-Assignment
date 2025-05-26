from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.utils import app
from api.serializer import ContainerSerializer,ContainerControlSerializer
from api.models import Container

from redis import Redis

redis_client = Redis(host='redis',port=6379,db=0)

class StartContainerAPIView(APIView):
    def post(self, request):
        serializer = ContainerSerializer(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                
                validated_data = serializer.validated_data
                user = validated_data['user']  
                image_name = validated_data['image_name']
                container_name = validated_data['container_name'] 
                print(user, image_name, container_name)
                task = app.send_task('api.tasks.start_ctf_container', args=[image_name, container_name])
                container_id = task.get()["container_id"]
                container_id_key = 'container_id_' + str(user.pk)
                redis_client.set(container_id_key, container_id)
                serializer.save()
                return Response({"message": "Container starting", "task_id": task.id, "Container_id":container_id}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": "You can not access more than one question "}, status=status.HTTP_409_CONFLICT)

class StopContainerAPIView(APIView):
    def post(self, request):
            serializer = ContainerControlSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                validated_data = serializer.validated_data
                user = validated_data['user']  
            container_id_key = 'container_id_' + str(user.pk)
            container_id = redis_client.get(container_id_key)
            if not container_id:
                return Response({"error": "container_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            container_id = container_id.decode()  


            if not container_id:
                return Response({"error": "container_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            task = app.send_task('api.tasks.stop_ctf_container', args=[container_id])
            return Response({"message": "Container Stopping", "task_id": task.id, "Container_id":container_id}, status=status.HTTP_202_ACCEPTED)



class RemoveConatinerAPIView(APIView):

    def post(self, request):
        serializer = ContainerControlSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            container = Container.objects.get(user=user)
            try:
                container.delete()
            except Exception as e:
                return Response({"error":"There is no Container"})
            
            container_id_key = 'container_id_' + str(user.pk)
            container_id = redis_client.get(container_id_key)
            
            if not container_id:
                return Response({"error": "container_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            container_id = container_id.decode()  


            if not container_id:
                return Response({"error": "container_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            task = app.send_task('api.tasks.remove_ctf_container', args=[container_id])
            return Response({"message": "Container Removing", "task_id": task.id, "Container_id":container_id}, status=status.HTTP_202_ACCEPTED)
        