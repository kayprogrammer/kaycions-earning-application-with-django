from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# Homepage model structures

class Contact(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    message = models.TextField(max_length=2000, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Suscribers(models.Model):
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return str(self.email)

# Custom User model structure

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(max_length=40, help_text='Email', null=True)
    full_name = models.CharField(max_length=40, help_text='Full name', null=True)
    twitter_id = models.CharField(max_length=30, help_text='Twitter ID', null=True)
    instagram_id = models.CharField(max_length=30, help_text='Instagram ID', null=True)
    youtube_id = models.CharField(max_length=40, help_text='Youtube ID', null=True)

# Dashboard model structures
class Worker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=False, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=40, help_text='Full name', null=True)
    email = models.EmailField(max_length=40, help_text='Email', null=True)
    twitter_id = models.CharField(max_length=30, help_text='Twitter ID', null=True)
    instagram_id = models.CharField(max_length=30, help_text='Instagram ID', null=True)
    youtube_id = models.CharField(max_length=40, help_text='Youtube ID', null=True)
    avatar = models.ImageField(upload_to='avatars', default="pro.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.full_name)

    @property
    def imageURL(self):
        try:
            url = self.avatar.url
        except:
            url = "/images/pro.png"
        return url

class AdminTask(models.Model):

    CATEGORY = (
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
        ('Like and Comment', 'Like and Comment'),
        ('Like, Comment and Share', 'Like, Comment and Share')

    )

    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    category_2 = models.CharField(max_length=200, null=True, choices=CATEGORY_2)
    description = models.TextField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    link = models.URLField(max_length=500, null=True)
    task_expiry_date = models.DateField(max_length=200, null=True)
    task_expiry_time = models.TimeField(null=True)
    worker = models.ManyToManyField(Worker)


    def __str__(self):
        return str(self.category + " " + self.category_2)

class TaskItem(models.Model):

    STATUS = (
        ('Pending','Pending'),
        ('Verified', 'Verified')
    )

    worker = models.ForeignKey(Worker, null=True, blank=True, on_delete=models.SET_NULL)
    task = models.ForeignKey(AdminTask, on_delete=models.SET_NULL, null=True)
    date_performed = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending')

    def __str__(self):
        return str(self.task)

class PaidTask(models.Model):

    worker = models.ForeignKey(Worker, null=True, blank=True, on_delete=models.SET_NULL)
    date_completed = models.DateTimeField(auto_now_add=True)
    payment_complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    @property
    def get_verifieditem_total(self):
        verifieditems = self.taskitem_set.all(status='Verified')
        total = sum([item.get_total for item in verifieditems])
        return total

'''
class RequestWithdrawal(models.Model):
    full_name = models.CharField(max_length=200, null=True)
    paypal_id = models.EmailField(max_length=200, null=True)
    withdrawal_amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
'''