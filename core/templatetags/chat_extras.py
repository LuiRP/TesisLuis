from django import template
from django.contrib.auth import get_user_model
import re
from django.utils.safestring import mark_safe

register = template.Library()
User = get_user_model()


@register.filter
def get_other_user(thread, current_user):
    if thread.user1 == current_user:
        return thread.user2
    return thread.user1


@register.filter
def linkify(text):
    meet_regex = re.compile(
        r"(https?:\/\/(meet\.new|meet\.google\.com\/\S+))", re.IGNORECASE
    )

    def replace_url(match):
        url = match.group(0)

        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'

    linked_text = meet_regex.sub(replace_url, text)

    linked_text = linked_text.replace("**", "<strong>")

    return mark_safe(linked_text)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
