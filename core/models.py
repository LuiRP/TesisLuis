from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    full_name = models.CharField("full name", max_length=254)
    email = models.EmailField("email address", max_length=254, unique=True)
    is_tutor = models.BooleanField(default=False)
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
