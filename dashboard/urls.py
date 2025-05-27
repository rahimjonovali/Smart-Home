from django.urls import path
from .views import ControlPanelView, RegisterView, BrokerEditView,ProfileEditView,SensorDataAPIView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('control/', ControlPanelView.as_view(), name='control-panel'),
    path('broker/', BrokerEditView.as_view(), name='broker-edit'),
    path('profile/', ProfileEditView.as_view(), name='profile'),
    path('api/sensor-data/', SensorDataAPIView.as_view(), name='sensor-data-api'),

]
