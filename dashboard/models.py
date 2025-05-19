from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Broker(models.Model):
    user     = models.OneToOneField(User, on_delete=models.CASCADE)
    host     = models.CharField("Host", max_length=200)
    port     = models.PositiveIntegerField("Port", default=1883)
    username = models.CharField("Username", max_length=100, blank=True)
    password = models.CharField("Password", max_length=100, blank=True)
    topic    = models.CharField("Topic", max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s broker"
