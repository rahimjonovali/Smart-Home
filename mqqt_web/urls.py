from django.urls import path
from .views import turn_on, turn_off

urlpatterns = [
    path('device/on/', turn_on, name='turn_on'),
    path('device/off/', turn_off, name='turn_off'),
]
