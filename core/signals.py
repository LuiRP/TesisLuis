from django.contrib.auth.models import Group
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def assign_group_on_signup(request, user, **kwargs):
    if user.is_tutor:
        group_name = "Tutors"
    else:
        group_name = "Users"

    try:
        target_group = Group.objects.get(name=group_name)
        user.groups.add(target_group)
        print(f"User {user.email} assigned to group '{group_name}'.")

    except Group.DoesNotExist:
        print(
            f"⚠️ Warning: Group '{group_name}' not found. Please ensure it is created via migration."
        )
