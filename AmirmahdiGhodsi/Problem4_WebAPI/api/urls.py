from django.urls import path
from .views import StartContainerAPIView, StopContainerAPIView,RemoveConatinerAPIView

urlpatterns = [
    path('start-container/', StartContainerAPIView.as_view(), name='start-container'),
    path('stop-container/', StopContainerAPIView.as_view(), name='stop-container'),
    path('remove-container/', RemoveConatinerAPIView.as_view(), name='remove-container'),

]