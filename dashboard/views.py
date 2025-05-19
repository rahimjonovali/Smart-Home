from django.views.generic import TemplateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import paho.mqtt.publish as publish
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class ControlPanelView(LoginRequiredMixin,TemplateView):
    template_name = "dashboard/control_panel.html"
    login_url = 'login'

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

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')