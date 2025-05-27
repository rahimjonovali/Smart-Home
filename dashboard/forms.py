from django import forms
from .models import Broker,Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class BrokerForm(forms.ModelForm):
    class Meta:
        model = Broker
        fields = ['host', 'port', 'username', 'password', 'topic']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }