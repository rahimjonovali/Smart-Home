from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile, SensorData

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        SensorData.objects.create(user=instance)
    else:
        instance.profile.save()
        # Create SensorData if it doesn't exist (for existing users)
        if not hasattr(instance, 'sensordata'):
            SensorData.objects.create(user=instance)