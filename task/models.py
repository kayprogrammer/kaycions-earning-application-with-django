from ctypes import addressof
import email
from email.policy import default
import imp
from urllib import request
from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from datetime import timedelta
from . utils import generate_ref_code
today = timezone.now

def f():
    return timezone.now() + timedelta(days=2)

# Create your models here.

# Homepage model structures

class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    message = models.TextField(max_length=2000, null=True)
    date_created = models.DateTimeField(default=today)

    def __str__(self):
        return str(self.name)

class Suscribers(models.Model):
    email = models.EmailField(max_length=200, null=True, unique=True)
    date_created = models.DateTimeField(default=today)

    def __str__(self):
        return str(self.email)

# Custom User model structure

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    terms_confirmed = models.BooleanField(null=False, blank=False, default=True)
    email = models.EmailField(_('email address'), max_length=40, help_text='Email', null=True, unique=True)
    full_name = models.CharField(max_length=40, help_text='Full name', null=True)
    code = models.CharField(max_length=60, blank=True)
    is_email_verified = models.BooleanField(default=False, null=True, blank=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return str(self.full_name)

# Dashboard model structures
class Worker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=False, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40, help_text='Full name', null=True)
    email = models.EmailField(max_length=40, help_text='Email', null=True, unique=True)
    facebook_id = models.CharField(max_length=30, help_text='Facebook ID', null=True, unique=True) 
    twitter_id = models.CharField(max_length=30, help_text='Twitter ID', null=True, unique=True)
    instagram_id = models.CharField(max_length=30, help_text='Instagram ID', null=True, unique=True)
    youtube_id = models.EmailField(max_length=40, help_text='Youtube ID', null=True, unique=True)
    paypal_address = models.EmailField(max_length=100, help_text='Paypal Address', null=True, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    code = models.TextField(blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='ref_by')
    date_created = models.DateTimeField(default=today)
    updated = models.DateTimeField(auto_now=True)

    def get_recommended_profiles(self):
        pass

    def save(self, *args, **kwargs):
        if self.code == "":
            full_name = self.full_name.replace(" ", "-").lower()
            code = generate_ref_code()
            self.code = str(full_name + "-" + code)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.full_name)

    @property
    def imageURL(self):
        try:
            url = self.avatar.url
        except:
            url = "https://res.cloudinary.com/kay-development/image/upload/v1643036318/avatars/pro_wqmqw5.png"
        return url

class Task(models.Model):

    CATEGORY = (
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Instagram', 'Instagram'),
        ('Youtube', 'Youtube'),
    )
    CATEGORY_2 = (
        ('Like', 'Like'),
        ('Share', 'Share'),
        ('Comment', 'Comment'),
        ('Mention', 'Mention'),
        ('Follow', 'Follow'),
        ('Repost', 'Repost'),
        ('Hastag', 'Hashtag'),
        ('Watch', 'Watch'),
        ('Re-tweet', 'Re-tweet'),
        ('Suscribe', 'Suscribe'),
        ('Like & Comment', 'Like & Comment'),

    )

    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    category_2 = models.CharField(max_length=200, null=True, choices=CATEGORY_2)
    description = models.TextField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    link = models.URLField(max_length=500, null=True)
    task_expiry_date = models.DateField(default=f, null=True)
    task_expiry_time = models.TimeField(default=today, null=True)
    worker = models.ForeignKey(Worker, related_name='tasks', on_delete=models.CASCADE, null=True, blank=True)
    pending = models.BooleanField(default=False, null=True, blank=True)
    completed = models.BooleanField(default=False, null=True, blank=True)
    disapproved = models.BooleanField(default=False, null=True, blank=True)
    who_updated = models.CharField(max_length=100, null=True, blank = True)


    def __str__(self):
        return str(self.category + " " + self.category_2)

    class Meta:
        ordering = ['-date_created']

class Earnings(models.Model):

    worker = models.ForeignKey(Worker, related_name='earnings', on_delete=models.CASCADE, null=True, blank=True)
    pending_earnings = models.DecimalField(default='0', max_digits=7, decimal_places=2, null=True, blank=True)
    verified_earnings = models.DecimalField(default='0', max_digits=7, decimal_places=2, null=True, blank=True)
    disapproved_earnings = models.DecimalField(default='0', max_digits=7, decimal_places=2, null=True, blank=True)
    withdrawn_earnings = models.DecimalField(default='0', max_digits=7, decimal_places=2, null=True, blank=True)
    paid_earnings = models.DecimalField(default='0', max_digits=7, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(default=today)

    def get_total_earnings(self):
        
        total = self.pending_earnings + self.verified_earnings + self.disapproved_earnings + self.withdrawn_earnings + self.paid_earnings
        
        return total

    def __str__(self):
        return str(self.worker)

class Withdrawal(models.Model):

    worker = models.ForeignKey(Worker, related_name='withdrawal', on_delete=models.CASCADE, null=True, blank=True)
    paypal_address = models.EmailField(max_length=100, null=True, blank=True)
    amount_withdraw = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    verified = models.BooleanField(default=False, null=True, blank=True)
    date_created = models.DateTimeField(default=today)

    def __str__(self):
        return str(self.worker)

    class Meta:
        ordering = ['-date_created']
        
class Complaints(models.Model):

    worker = models.ForeignKey(Worker, related_name='complaints', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=5000, null=True, blank=True)
    date_created = models.DateTimeField(default=today)

    def __str__(self):
        return str(self.worker)

class About(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField(max_length=8000, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    whatsapp = models.CharField(max_length=30, null=True, blank=True)
    whatsapp_link = models.URLField(max_length=300, null=True, blank=True)
    address = models.TextField(max_length=400, null=True, blank=True)
    facebook = models.CharField(max_length=700, null=True, blank=True)
    facebook_link = models.URLField(max_length=700, null=True, blank=True)
    twitter = models.CharField(max_length=700, null=True, blank=True)
    twitter_link = models.URLField(max_length=700, null=True, blank=True)
    instagram = models.CharField(max_length=700, null=True, blank=True)
    instagram_link = models.URLField(max_length=700, null=True, blank=True)
    linkedin = models.CharField(max_length=700, null=True, blank=True)
    linkedin_link = models.URLField(max_length=700, null=True, blank=True)

    def __str__(self):
        return 'About Details'

class Notification(models.Model):
#   1 = welcome notification, 2 = New Task Created, 3 = Task Updated, 4 = attempt task, 5 = verified earning, 6 = verify disapproved task
#   7 = disapprove pending tasks, 8 = disapproved verified tasks, 9 = send withdrawal request, 10 = approve withdrawal request, 11 = referral notifications
    notification_type = models.IntegerField()
    to_worker = models.ForeignKey(Worker, related_name='notification_to', on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey(Worker, related_name='notification_to2', on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    earning = models.ForeignKey('Earnings', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    withdrawal = models.ForeignKey('Withdrawal', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    worker_has_seen = models.BooleanField(default=False)

class Faqs_Terms(models.Model):
    faqs_title = models.CharField(max_length=100, null=True, blank=True)
    terms_title = models.CharField(max_length=100, null=True, blank=True)
    faqs_text = models.TextField(max_length=5000, null=True, blank=True)
    terms_text = models.TextField(max_length=5000, null=True, blank=True)



