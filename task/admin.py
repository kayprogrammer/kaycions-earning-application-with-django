from django.contrib import admin
from . models import *
# Register your models here.

MyModels = [User, Contact, Suscribers, Worker, AdminTask, TaskItem, PaidTask,]
admin.site.register(MyModels)
