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
    description = models.TextField("description", blank=True)

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
    COURSE_CHOICES = [
        ("calculo_i", "Cálculo I"),
        ("logica", "Lógica"),
        ("calculo_ii", "Cálculo II"),
        ("introduccion_a_la_informatica", "Introducción a la Informática"),
        ("estadistica_descriptiva", "Estadística Descriptiva"),
        ("ingles_instrumental", "Inglés Instrumental"),
        ("calculo_iii", "Cálculo III"),
        ("fisica", "Física"),
        ("algoritmos_y_programacion_i", "Algoritmos y Programación I"),
        ("algebra", "Álgebra"),
        ("inferencia_y_probabilidades", "Inferencia y Probabilidades"),
        ("calculo_iv", "Cálculo IV"),
        ("estructuras_discretas", "Estructuras Discretas"),
        ("algoritmos_y_programacion_ii", "Algoritmos y Programación II"),
        ("electronica", "Electrónica"),
        ("bases_de_datos_i", "Bases de Datos I"),
        ("algoritmos_y_programacion_iii", "Algoritmos y Programación III"),
        ("bases_de_datos_ii", "Bases de Datos II"),
        ("metodos_numericos", "Métodos Numéricos"),
        (
            "principios_de_ingenieria_del_software",
            "Principios de Ingeniería del Software",
        ),
        ("arquitecturas_software", "Arquitecturas Software"),
        (
            "metodologias_de_desarrollo_de_software",
            "Metodologías de Desarrollo de Software",
        ),
        ("redes_y_comunicaciones_i", "Redes y Comunicaciones I"),
        ("desarrollo_de_aplicaciones_i", "Desarrollo de Aplicaciones I"),
        ("redes_y_comunicaciones_ii", "Redes y Comunicaciones II"),
        ("desarrollo_de_aplicaciones_ii", "Desarrollo de Aplicaciones II"),
    ]
    name = models.CharField("Nombre de la tutoria", choices=COURSE_CHOICES)
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


class Period(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tutor"
    )
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    day = models.DateField(auto_now=False, auto_now_add=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="student",
    )
