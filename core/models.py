from django.contrib.auth.models import (
    AbstractUser,
    UserManager,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    full_name = models.CharField("full name", max_length=254)
    email = models.EmailField("email address", max_length=254, unique=True)
    is_tutor = models.BooleanField(default=False)

    profile_picture = models.ImageField(
        upload_to="profile_pics/",
        null=True,
        blank=True,
        default="profile_pics/default.jpg",
    )

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Tutorship(models.Model):
    name = models.CharField("Nombre de la tutoria", max_length=254)
    tutor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.TextField("Descripcion de la tutoria")
    created_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="authored_reviews"
    )
    reviewed = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="received_reviews"
    )
    body = models.TextField("Cuerpo de la reseña")
    rating = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatThread(models.Model):
    user1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="chat_threads_as_user1"
    )
    user2 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="chat_threads_as_user2"
    )

    class Meta:
        unique_together = ("user1", "user2")

    def get_ordered_users(self):
        return sorted([self.user1, self.user2], key=lambda u: u.id)

    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"


class Message(models.Model):
    thread = models.ForeignKey(
        ChatThread, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("timestamp",)

    def __str__(self):
        return (
            f"Message by {self.sender.username} at {self.timestamp.strftime('%H:%M')}"
        )
