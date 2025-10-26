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