from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .mqtt_client import send_mqtt_command

# @api_view(['POST'])
# def turn_on(request):
#     send_mqtt_command("ON")
#     return Response({"status": "Device turned ON"})

# @api_view(['POST'])
# def turn_off(request):
#     send_mqtt_command("OFF")
#     return Response({"status": "Device turned OFF"})


@api_view(['POST'])
def control_device(request):
    action = request.data.get("action", "").upper()
    
    if action == "ON":
        send_mqtt_command("ON")
        return Response({"status": "Device turned ON"})
    elif action == "OFF":
        send_mqtt_command("OFF")
        return Response({"status": "Device turned OFF"})
    else:
        return Response(
            {"error": "Invalid action. Use 'ON' or 'OFF'."},
            status=status.HTTP_400_BAD_REQUEST
        )
