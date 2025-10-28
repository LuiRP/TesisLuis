from django.db import migrations
from django.core.management.sql import emit_post_migrate_signal


def setup_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    emit_post_migrate_signal(2, False, "default")

    tutor_perms = [
        # Tutorship Permissions
        "add_tutorship",
        "change_tutorship",
        "delete_tutorship",
        "view_tutorship",
        "view_review",
    ]

    user_perms = [
        "add_review",
        "change_review",
        "delete_review",
        "view_review",
        "view_tutorship",
    ]

    tutors_group, created = Group.objects.get_or_create(name="Tutors")

    if created or tutors_group.permissions.count() == 0:
        tutor_permission_objects = Permission.objects.filter(codename__in=tutor_perms)
        tutors_group.permissions.set(tutor_permission_objects)
        print("Tutors group created and permissions assigned.")

    users_group, created = Group.objects.get_or_create(name="Users")

    if created or users_group.permissions.count() == 0:
        user_permission_objects = Permission.objects.filter(codename__in=user_perms)
        users_group.permissions.set(user_permission_objects)
        print("Users group created and permissions assigned.")


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Tutors", "Users"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("core", "0004_tutorship"),
        ("core", "0007_review"),
        ("core", "0008_customuser_profile_picture"),
    ]

    operations = [
        migrations.RunPython(setup_groups_and_permissions, remove_groups),
    ]
