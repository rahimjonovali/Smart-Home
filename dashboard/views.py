from django.views.generic import TemplateView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
import paho.mqtt.publish as publish
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Broker
from .forms import BrokerForm

class ControlPanelView(TemplateView):
    template_name = "dashboard/control_panel.html"

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        if action in ["ON", "OFF"]:
            broker = Broker.objects.get(user=request.user)
            publish.single(
                topic=broker.topic,
                payload=action,
                hostname=broker.host,
                port=broker.port,
                auth={'username': broker.username, 'password': broker.password}
            )
        return self.render_to_response(self.get_context_data())


class BrokerEditView(LoginRequiredMixin, UpdateView):
    model = Broker
    form_class = BrokerForm
    template_name = 'dashboard/broker_form.html'
    success_url = reverse_lazy('control-panel')

    def get_object(self, queryset=None):
        # Return or create this user's Broker instance
        obj, created = Broker.objects.get_or_create(user=self.request.user)
        return obj


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')