from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AddUser  

router = DefaultRouter()
router.register(r'add-user', AddUser, basename='add-user')

urlpatterns = [ 
]

urlpatterns += router.urls