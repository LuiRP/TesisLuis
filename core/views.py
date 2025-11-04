from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from . import models
from . import forms
from django.db.models import Q, Max, F
from datetime import datetime
from collections import defaultdict

DAY_MAP = {
    "lunes": "lunes_date",
    "martes": "martes_date",
    "miercoles": "miercoles_date",
    "jueves": "jueves_date",
    "viernes": "viernes_date",
    "sabado": "sabado_date",
    "domingo": "domingo_date",
}

WEEKDAYS_SPANISH = {
    0: "lunes",
    1: "martes",
    2: "miercoles",
    3: "jueves",
    4: "viernes",
    5: "sabado",
    6: "domingo",
}


# Create your views here.
def index(request):
    return render(request, "index.html")


@login_required
def tutorships(request):
    search_query = request.GET.get("search", "")

    show_my_tutorships = request.GET.get("my_tutorships") == "on"

    tutorships_list = models.Tutorship.objects.all()

    if show_my_tutorships and request.user.is_authenticated:
        tutorships_list = tutorships_list.filter(tutor=request.user)

    if search_query:
        from django.db.models import Q

        tutorships_list = tutorships_list.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    tutorships_list = tutorships_list.order_by("created_at")

    paginator = Paginator(tutorships_list, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tutorship/index.html",
        {"page_obj": page_obj, "search_query": search_query},
    )


@login_required
@permission_required("core.add_tutorship", raise_exception=True)
def create_tutorship(request):
    if request.method == "POST":
        form = forms.TutorshipForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"].strip()
            tutor = request.user
            t = models.Tutorship(name=name, description=description, tutor=tutor)
            t.save()
            return HttpResponseRedirect("/tutorship")
    else:
        form = forms.TutorshipForm()
    return render(request, "tutorship/create.html", {"form": form})


@login_required
@permission_required("core.change_tutorship", raise_exception=True)
def edit_tutorship(request, pk):
    tutorship = get_object_or_404(models.Tutorship, pk=pk)
    if tutorship.tutor != request.user:
        raise PermissionDenied()
    if request.method == "POST":
        form = forms.TutorshipForm(request.POST)
        if form.is_valid():
            tutorship.name = form.cleaned_data["name"]
            tutorship.description = form.cleaned_data["description"].strip()
            tutorship.save()
            return HttpResponseRedirect("/tutorship")
    else:
        initial_data = {
            "name": tutorship.name,
            "description": tutorship.description.strip(),
        }
        form = forms.TutorshipForm(initial=initial_data)
    print(initial_data)
    return render(
        request,
        "tutorship/edit.html",
        {"form": form, "tutorship": tutorship},
    )


@login_required
@permission_required("core.delete_tutorship", raise_exception=True)
def delete_tutorship(request, pk):
    tutorship = get_object_or_404(models.Tutorship, pk=pk)
    if tutorship.tutor != request.user:
        raise PermissionDenied()
    if request.method == "POST":
        tutorship.delete()
        return HttpResponseRedirect("/tutorship")
    return HttpResponseRedirect("/tutorship")


@login_required
def public_user(request, pk):
    tutor = get_object_or_404(models.CustomUser, pk=pk)

    reviews = models.Review.objects.filter(reviewed=tutor).order_by("-created_at")
    paginator = Paginator(reviews, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/public.html",
        {"tutor": tutor, "page_obj": page_obj},
    )


@login_required
@permission_required("core.add_review", raise_exception=True)
def create_review(request, pk):
    reviewed = get_object_or_404(models.CustomUser, pk=pk)
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data["body"]
            rating = form.cleaned_data["rating"]
            author = request.user
            t = models.Review(
                body=body, author=author, rating=rating, reviewed=reviewed
            )
            t.save()

            redirect_url = reverse("public_user", kwargs={"pk": reviewed.pk})
            return HttpResponseRedirect(redirect_url)
    else:
        form = forms.ReviewForm()
    return render(request, "review/create.html", {"form": form, "tutor": reviewed})


@login_required
@permission_required("core.change_review", raise_exception=True)
def edit_review(request, pk):
    review_to_edit = get_object_or_404(models.Review, pk=pk)
    if review_to_edit.author != request.user:
        raise PermissionDenied()

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)

        if form.is_valid():
            review_to_edit.body = form.cleaned_data["body"]
            review_to_edit.rating = form.cleaned_data["rating"]
            review_to_edit.save()

            redirect_url = reverse(
                "public_user", kwargs={"pk": review_to_edit.reviewed.pk}
            )
            return HttpResponseRedirect(redirect_url)
    else:
        initial_data = {
            "body": review_to_edit.body,
            "rating": review_to_edit.rating,
        }
        form = forms.ReviewForm(initial=initial_data)

    return render(
        request,
        "review/edit.html",
        {
            "form": form,
            "reviewed": review_to_edit,
        },
    )


@login_required
@permission_required("core.delete_review", raise_exception=True)
def delete_review(request, pk):
    review = get_object_or_404(models.Review, pk=pk)
    if review.author != request.user:
        raise PermissionDenied()
    if request.method == "POST":
        review.delete()
        redirect_url = reverse("public_user", kwargs={"pk": review.reviewed.pk})
        return HttpResponseRedirect(redirect_url)
    redirect_url = reverse("public_user", kwargs={"pk": review.reviewed.pk})
    return HttpResponseRedirect(redirect_url)


@login_required
def private_profile(request):
    return render(request, "profile/private.html")


@login_required
def profile_update_view(request):
    user = request.user
    if request.method == "POST":
        form = forms.UserProfileUpdateForm(request.POST, request.FILES)

        if form.is_valid():
            new_full_name = form.cleaned_data["full_name"]
            new_profile_picture = form.cleaned_data.get("profile_picture")
            user.full_name = new_full_name
            if new_profile_picture:
                user.profile_picture = new_profile_picture
            user.save()
            return redirect("private_profile")
    else:
        initial_data = {
            "full_name": user.full_name,
        }
        form = forms.UserProfileUpdateForm(initial=initial_data)
    return render(request, "profile/edit.html", {"form": form})


@login_required
def get_or_create_chat_thread(request, other_user_id):
    current_user = request.user
    other_user = get_object_or_404(models.CustomUser, id=other_user_id)

    if current_user == other_user:
        return redirect("inbox")

    try:
        thread = models.ChatThread.objects.get(
            Q(user1=current_user, user2=other_user)
            | Q(user1=other_user, user2=current_user)
        )
    except models.ChatThread.DoesNotExist:
        if current_user.id < other_user.id:
            thread = models.ChatThread.objects.create(
                user1=current_user, user2=other_user
            )
        else:
            thread = models.ChatThread.objects.create(
                user1=other_user, user2=current_user
            )

    messages = thread.messages.all()

    recent_threads = (
        models.ChatThread.objects.filter(Q(user1=current_user) | Q(user2=current_user))
        .annotate(last_message_time=Max("messages__timestamp"))
        .order_by(
            F("last_message_time").desc(nulls_last=True),
            "-id",
        )
    )
    context = {
        "thread": thread,
        "other_user": other_user,
        "messages": messages,
        "recent_threads": recent_threads,
    }
    return render(request, "chat/chat.html", context)


@login_required
def inbox_view(request):
    current_user = request.user
    recent_threads = (
        models.ChatThread.objects.filter(Q(user1=current_user) | Q(user2=current_user))
        .annotate(last_message_time=Max("messages__timestamp"))
        .order_by(
            F("last_message_time").desc(nulls_last=True),
            "-id",
        )
    )
    context = {
        "recent_threads": recent_threads,
    }
    return render(request, "chat/inbox.html", context)


@login_required
def timetable(request):
    user = request.user

    is_tutor = getattr(user, "is_tutor", False)

    if is_tutor:
        periods_queryset = models.Period.objects.filter(owner=user).order_by(
            "day", "start_time"
        )
        schedule_title = "Mi Horario Completo"
    else:
        periods_queryset = models.Period.objects.filter(student=user).order_by(
            "day", "start_time"
        )
        schedule_title = "Mis Clases Inscritas"
    periods_by_day = {}
    for period in periods_queryset:
        day_key = period.day
        if day_key not in periods_by_day:
            periods_by_day[day_key] = []
        periods_by_day[day_key].append(period)

    sorted_days = sorted(periods_by_day.keys())

    context = {
        "periods_by_day": periods_by_day,
        "sorted_days": sorted_days,
        "is_tutor": is_tutor,
        "schedule_title": schedule_title,
    }

    return render(request, "timetable/index.html", context)


@login_required
def create_timetable(request):
    if request.method == "POST":
        models.Period.objects.filter(owner=request.user, student__isnull=True).delete()

        periods_to_create = []

        for day, date_field_name in DAY_MAP.items():
            day_date_str = request.POST.get(date_field_name)

            if not day_date_str:
                continue

            day_date = datetime.strptime(day_date_str, "%Y-%m-%d").date()
            start_times = request.POST.getlist(f"periods[{day}][start][]")
            end_times = request.POST.getlist(f"periods[{day}][end][]")

            if len(start_times) != len(end_times):
                print(f"Mismatch in start/end times for {day}")
                continue

            for start_time_str, end_time_str in zip(start_times, end_times):
                if start_time_str and end_time_str:
                    try:
                        start_time = datetime.strptime(start_time_str, "%H:%M").time()
                        end_time = datetime.strptime(end_time_str, "%H:%M").time()

                        if start_time >= end_time:
                            print(
                                f"Invalid time range skipped for {day}: {start_time_str} - {end_time_str}"
                            )
                            continue

                        period = models.Period(
                            owner=request.user,
                            start_time=start_time,
                            end_time=end_time,
                            day=day_date,
                            student=None,
                        )
                        periods_to_create.append(period)
                    except ValueError:
                        continue

        models.Period.objects.bulk_create(periods_to_create)

        return redirect("timetable")
    existing_periods = models.Period.objects.filter(owner=request.user).order_by(
        "day", "start_time"
    )

    existing_periods_data = defaultdict(list)

    for period in existing_periods:
        day_index = period.day.weekday()
        day_name = WEEKDAYS_SPANISH.get(day_index, "unknown")

        is_booked = period.student is not None
        student_name = (
            period.student.full_name
            if period.student and hasattr(period.student, "full_name")
            else (period.student.username if period.student else None)
        )

        existing_periods_data[day_name].append(
            {
                "pk": period.pk,
                "start_time": period.start_time.strftime("%H:%M"),
                "end_time": period.end_time.strftime("%H:%M"),
                "is_booked": is_booked,
                "student_name": student_name,
            }
        )

    context = {
        "existing_periods_data": existing_periods_data,
        "DAY_MAP_ITEMS": DAY_MAP.items(),
    }

    return render(request, "timetable/create.html", context)


@login_required
def tutor_schedule_select(request, pk):

    tutor = get_object_or_404(models.CustomUser, pk=pk)

    if request.user == tutor:
        pass

    available_periods = models.Period.objects.filter(
        owner=tutor, student__isnull=True
    ).order_by("day", "start_time")

    periods_by_day = defaultdict(list)
    for period in available_periods:
        periods_by_day[period.day].append(period)

    sorted_days = sorted(periods_by_day.keys())

    context = {
        "tutor": tutor,
        "periods_by_day": periods_by_day,
        "sorted_days": sorted_days,
    }

    return render(request, "timetable/tutor_schedule_select.html", context)


login_required


def book_period(request, pk):
    period = get_object_or_404(models.Period, pk=pk)

    if period.student is not None:
        return redirect("timetable")

    if period.owner == request.user:
        return redirect("timetable")

    period.student = request.user
    period.save()
    return redirect("timetable")


@login_required
def cancel_period(request, pk):
    if request.method != "POST":
        return redirect("timetable")

    period = get_object_or_404(models.Period, pk=pk)
    user = request.user

    is_owner = period.owner == user
    is_student = period.student == user

    if not is_owner and not is_student:
        return redirect("timetable")

    if period.student is None:
        return redirect("timetable")

    period.student = None
    period.save()

    return redirect("timetable")
