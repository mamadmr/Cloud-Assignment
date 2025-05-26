from django.urls import path
from .views import AssignContainer, RemoveContainer, ContainerList

urlpatterns = [
    path("assign/", AssignContainer.as_view(), name="assign-container"),
    path("remove/", RemoveContainer.as_view(), name="remove-container"),
    path("list/", ContainerList.as_view(), name="container-list"),
]
