from django import forms
from .models import Broker

class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['host', 'port', 'username', 'password', 'topic']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
