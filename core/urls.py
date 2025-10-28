from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tutorship/", views.tutorships, name="tutorship"),
    path("tutorship/create", views.create_tutorship, name="create_tutorship"),
    path("tutorship/edit/<int:pk>", views.edit_tutorship, name="edit_tutorship"),
    path("tutorship/delete/<int:pk>/", views.delete_tutorship, name="delete_tutorship"),
]
