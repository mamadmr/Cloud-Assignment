from django.urls import path
from .views import (
    AssignChallenge,
    RemoveChallenge,
    ActiveContainerInfo,
)

urlpatterns = [
    path('assign/', AssignChallenge.as_view(), name='assign-challenge'),
    path('remove/', RemoveChallenge.as_view(), name='remove-challenge'),
    path('container-info/', ActiveContainerInfo.as_view(), name='container-info'),
]
