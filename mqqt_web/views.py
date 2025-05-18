from rest_framework.decorators import api_view
from rest_framework.response import Response
from .mqtt_client import send_mqtt_command

@api_view(['POST'])
def turn_on(request):
    send_mqtt_command("ON")
    return Response({"status": "Device turned ON"})

@api_view(['POST'])
def turn_off(request):
    send_mqtt_command("OFF")
    return Response({"status": "Device turned OFF"})

