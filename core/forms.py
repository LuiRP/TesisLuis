from django import forms
from . import models


class ExpandedSignUpForm(forms.Form):
    is_tutor = forms.BooleanField(required=False, label="Tutor")
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={"placeholder": "Nombre"}),
    )
    field_order = ["full_name", "email", "password1", "password2", "is_tutor"]

    def signup(self, request, user):
        user.full_name = self.cleaned_data["full_name"]
        user.is_tutor = self.cleaned_data["is_tutor"]
        user.save()


class TutorshipForm(forms.Form):
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
    name = forms.ChoiceField(choices=COURSE_CHOICES, required=True, label="Materia")
    description = forms.CharField(label="Descripcion", widget=forms.Textarea)


class ReviewForm(forms.Form):
    body = forms.CharField(label="Descripcion", widget=forms.Textarea)
    rating = forms.IntegerField(label="Calificación", max_value=5, min_value=0)


class UserProfileUpdateForm(forms.Form):
    full_name = forms.CharField(label="Nombre Completo", max_length=254)
    profile_picture = forms.ImageField(
        label="Imagen de perfil",
        required=False,
        widget=forms.FileInput,
    )
    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ingresa tu descripción",
                "rows": 2,
                "class": "textarea textarea-bordered w-full",
            }
        ),
    )
