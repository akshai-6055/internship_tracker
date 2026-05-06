from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Internship, Application

@receiver(post_save, sender=Internship)
def internship_created(sender, instance, created, **kwargs):
    if created:
        # Here you could trigger notifications or logging
        print(f"DEBUG: New Internship created: {instance.title} by {instance.employer}")

@receiver(post_save, sender=Application)
def application_status_changed(sender, instance, created, **kwargs):
    if not created:
        # If status was updated
        # Here you could trigger an email or notification to the student
        print(f"DEBUG: Application status for {instance.user.username} changed to {instance.status}")
