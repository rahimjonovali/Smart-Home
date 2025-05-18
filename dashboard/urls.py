from django.urls import path
from .views import ControlPanelView

urlpatterns = [
    path('', ControlPanelView.as_view(), name='control-panel'),
]
