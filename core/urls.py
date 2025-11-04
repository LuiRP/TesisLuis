from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("tutorship/", views.tutorships, name="tutorship"),
    path("tutorship/create", views.create_tutorship, name="create_tutorship"),
    path("tutorship/edit/<int:pk>", views.edit_tutorship, name="edit_tutorship"),
    path("tutorship/delete/<int:pk>/", views.delete_tutorship, name="delete_tutorship"),
    path("user/<int:pk>/", views.public_user, name="public_user"),
    path("review/create/<int:pk>", views.create_review, name="create_review"),
    path("review/edit/<int:pk>", views.edit_review, name="edit_review"),
    path("review/delete/<int:pk>/", views.delete_review, name="delete_review"),
    path("account/profile", views.private_profile, name="private_profile"),
    path("account/edit/profile", views.profile_update_view, name="profile_update_view"),
    path("inbox/", views.inbox_view, name="inbox"),
    path(
        "chat/<int:other_user_id>/", views.get_or_create_chat_thread, name="start_chat"
    ),
    path("timetable/", views.timetable, name="timetable"),
    path("timetable/create", views.create_timetable, name="create_timetable"),
    path(
        "tutor/<int:pk>/schedule/select/",
        views.tutor_schedule_select,
        name="tutor_schedule_select",
    ),
    path("period/<int:pk>/book/", views.book_period, name="book_period"),
    path("period/<int:pk>/cancel/", views.cancel_period, name="cancel_period"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
