from django import template
from task.models import Notification, Worker

register = template.Library()


@register.inclusion_tag('task/show_notifications.html', takes_context=True)
def show_notifications(context):
    request_user = context['request'].user
    if not request_user.is_staff:
        worker = Worker.objects.filter(user__is_staff=False).get(user=request_user)
        notifications = Notification.objects.filter(to_worker=worker).exclude(admin__isnull=False).exclude(worker_has_seen=True).order_by('-date')
    else:
        admin = Worker.objects.filter(user__is_staff=True).get(user=request_user)
        notifications = Notification.objects.filter(admin=admin).exclude(worker_has_seen=True).order_by('-date')
    not_count = notifications.count()
    return {'notifications': notifications, 'nc':not_count}