from django.views.generic import TemplateView,CreateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
import paho.mqtt.publish as publish
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Broker,Profile
from .forms import BrokerForm,UserForm,ProfileForm

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


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = 'dashboard/profile_form.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return self.render_to_response({
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.success_url)
        return self.render_to_response({
            'user_form': user_form,
            'profile_form': profile_form
        })