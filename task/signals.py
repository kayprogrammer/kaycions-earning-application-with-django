from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User, Group
from . models import Worker

def worker_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='worker')
        instance.groups.add(group)

        Worker.objects.create(user=instance, full_name=instance.full_name, email=instance.email)
        print('Profile Created!')

post_save.connect(worker_profile, sender=settings.AUTH_USER_MODEL)