from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import Worker
from django.contrib.auth.models import User, Group

def worker_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='worker')
        instance.groups.add(group)
        if instance.referral_code != "":
            Worker.objects.create(user=instance, full_name=instance.full_name, email=instance.email, recommended_by = Worker.objects.get(code=instance.referral_code).user)
        else:
            Worker.objects.create(user=instance, full_name=instance.full_name, email=instance.email, recommended_by = None)
        print('Profile Created!')

post_save.connect(worker_profile, sender=settings.AUTH_USER_MODEL)
