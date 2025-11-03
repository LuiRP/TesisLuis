from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


@register.filter
def get_other_user(thread, current_user):
    if thread.user1 == current_user:
        return thread.user2
    return thread.user1
