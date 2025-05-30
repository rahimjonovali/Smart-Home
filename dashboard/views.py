from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import JsonResponse
import paho.mqtt.publish as publish
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Broker, Profile, SensorData
from .forms import BrokerForm, UserForm, ProfileForm
from .mqtt_service import mqtt_service
import socket
from socket import timeout as SocketTimeout
import json

class ControlPanelView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/control_panel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create sensor data for current user
        sensor_data, created = SensorData.objects.get_or_create(user=self.request.user)
        context['sensor_data'] = sensor_data
        
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        mode = request.POST.get("mode")
        
        # Get or create sensor data
        sensor_data, created = SensorData.objects.get_or_create(user=request.user)
        
        # Handle mode change
        if mode:
            sensor_data.control_mode = mode
            sensor_data.save()
        
        # Handle lamp control
        if action in ["ON", "OFF"]:
            try:
                broker = Broker.objects.get(user=request.user)
                
                # Set socket-level timeout
                socket.setdefaulttimeout(0.1)  # seconds
                
                publish.single(
                    topic=broker.topic,
                    payload=action,
                    hostname=broker.host,
                    port=broker.port,
                    auth={'username': broker.username, 'password': broker.password}
                )
                
                # Update lamp status
                sensor_data.lamp_status = (action == "ON")
                sensor_data.save()
                
            except Broker.DoesNotExist:
                context = self.get_context_data()
                context["error"] = "Please configure your MQTT broker first."
                return self.render_to_response(context)
            except SocketTimeout:
                context = self.get_context_data()
                context["error"] = "Connection to broker timed out."
                return self.render_to_response(context)
            except Exception as e:
                context = self.get_context_data()
                context["error"] = f"An error occurred: {str(e)}"
                return self.render_to_response(context)
            finally:
                socket.setdefaulttimeout(None)

        return self.render_to_response(self.get_context_data())

class SensorDataAPIView(LoginRequiredMixin, TemplateView):
    """API endpoint to get real-time sensor data"""
    
    def get(self, request, *args, **kwargs):
        try:
            sensor_data = SensorData.objects.get(user=request.user)
            data = {
                'lamp_status': sensor_data.lamp_status,
                'control_mode': sensor_data.control_mode,
                'photoresistor_value': sensor_data.photoresistor_value,
                'pir_motion_detected': sensor_data.pir_motion_detected,
                'pir_status_text': sensor_data.pir_status_text,
                'last_updated': sensor_data.last_updated.isoformat()
            }
            return JsonResponse(data)
        except SensorData.DoesNotExist:
            return JsonResponse({'error': 'Sensor data not found'}, status=404)

class BrokerEditView(LoginRequiredMixin, UpdateView):
    model = Broker
    form_class = BrokerForm
    template_name = 'dashboard/broker_form.html'
    success_url = reverse_lazy('control-panel')

    def get_object(self, queryset=None):
        # Return or create this user's Broker instance
        obj, created = Broker.objects.get_or_create(user=self.request.user)
        return obj
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Start MQTT listener for this user after saving broker config
        try:
            mqtt_service.create_client_for_user(self.object)
        except Exception as e:
            # Log error but don't fail the form submission
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to start MQTT client: {e}")
        return response

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