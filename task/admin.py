from django.contrib import admin
from . models import *
# Register your models here.
'''
MyModels = [User, Contact, Suscribers, Worker, AdminTask]
'''
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('unique_code', 'clicked', )

admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Suscribers)
admin.site.register(Worker)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskItem, TaskAdmin)
admin.site.register(Earnings)
admin.site.register(Withdrawal)
admin.site.register(Complaints)
admin.site.register(About)
admin.site.register(Notification)
admin.site.register(Faqs_Terms)

