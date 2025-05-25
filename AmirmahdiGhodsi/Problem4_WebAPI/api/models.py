from django.db import models
from main_app.models import User

# Create your models here.
class Container(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=255)
    container_name = models.CharField(max_length=255)
