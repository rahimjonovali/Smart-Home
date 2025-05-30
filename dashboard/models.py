from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
User = get_user_model()

class Broker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    host = models.CharField("Host", max_length=200)
    port = models.PositiveIntegerField("Port", default=1883)
    username = models.CharField("Username", max_length=100, blank=True)
    password = models.CharField("Password", max_length=100, blank=True)
    topic = models.CharField("Topic", max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s broker"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField("Full Name", max_length=20, blank=True)
    email = models.EmailField("Email", max_length=20, blank=True)
    birth_date = models.DateField("Birth Date", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class SensorData(models.Model):
    CONTROL_MODES = [
        ('manual', 'Mode 1 - Manual'),
        ('pir', 'Mode 2 - PIR Motion'),
        ('photoresistor', 'Mode 3 - Photoresistor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lamp_status = models.BooleanField("Lamp Status", default=False)
    control_mode = models.CharField("Control Mode", max_length=20, choices=CONTROL_MODES, default='manual')
    photoresistor_value = models.IntegerField("Photoresistor Value", default=0)
    pir_motion_detected = models.BooleanField("PIR Motion Detected", default=False)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s sensor data"
    
    @property
    def pir_status_text(self):
        return "Motion detected" if self.pir_motion_detected else "No motion"