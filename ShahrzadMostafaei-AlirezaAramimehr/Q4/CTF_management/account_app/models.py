from django.db import models
from auth_app.models import User

# Create your models here.
class Container(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255)
    container_name = models.CharField(max_length=255)
    port = models.IntegerField(null=True, blank=True)
