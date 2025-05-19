from django.urls import path
from .views import ControlPanelView, RegisterView, BrokerEditView

urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('control/', ControlPanelView.as_view(), name='control-panel'),
    path('broker/', BrokerEditView.as_view(), name='broker-edit'),
]
