from django import template
from notifications.models import Notification

register = template.Library()


@register.simple_tag
def unread_notification(user):
    notification_count = Notification.objects.filter(
        is_seen=False, to_user=user
    ).count()
    return notification_count
