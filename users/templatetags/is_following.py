from django import template
from users.models import Follow

register = template.Library()


@register.simple_tag
def is_following(from_user, to_user):
    is_following = Follow.objects.filter(from_user=from_user, to_user=to_user)
    is_following = True if is_following else False
    return is_following
