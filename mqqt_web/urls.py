from django.urls import path
from .views import control_device

urlpatterns = [
    # path('device/on/', turn_on, name='turn_on'),
    # path('device/off/', turn_off, name='turn_off'),
    path('control', control_device, name='control_device'),
]
