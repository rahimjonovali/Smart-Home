from django.views.generic import TemplateView
from django.shortcuts import render
import paho.mqtt.publish as publish

class ControlPanelView(TemplateView):
    template_name = "dashboard/control_panel.html"

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")

        if action in ["ON", "OFF"]:
            publish.single(
                topic="home/relay1/control",
                payload=action,
                hostname="206.189.51.153",
                port=1883,
                auth={"username": "userA", "password": "12345678913"}
            )

        return render(request, self.template_name)
