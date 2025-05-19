from django.urls import path
from .views import ControlPanelView,RegisterView

urlpatterns = [
    # path('', ControlPanelView.as_view(), name='control-panel'),
    path('', RegisterView.as_view(), name='register'),
]
