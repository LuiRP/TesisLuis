from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import models
from . import forms


# Create your views here.
def index(request):
    return render(request, "index.html")


@login_required
def tutorships(request):
    tutorships = models.Tutorship.objects.all().order_by("created_at")
    paginator = Paginator(tutorships, 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tutorship/index.html", {"page_obj": page_obj})


@login_required
def create_tutorship(request):
    if request.method == "POST":
        form = forms.TutorshipForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            tutor = request.user
            t = models.Tutorship(name=name, description=description, tutor=tutor)
            t.save()
            return HttpResponseRedirect("/tutorship")
    else:
        form = forms.TutorshipForm()
    return render(request, "tutorship/create.html", {"form": form})


@login_required
def edit_tutorship(request, pk):
    tutorship = get_object_or_404(models.Tutorship, pk=pk)
    if request.method == "POST":
        form = forms.TutorshipForm(request.POST)
        if form.is_valid():
            tutorship.name = form.cleaned_data["name"]
            tutorship.description = form.cleaned_data["description"]
            tutorship.save()
            return HttpResponseRedirect("/tutorship")
    else:
        initial_data = {
            "name": tutorship.name,
            "description": tutorship.description,
        }
        form = forms.TutorshipForm(initial=initial_data)
    return render(
        request,
        "tutorship/edit.html",
        {"form": form, "tutorship": tutorship},
    )


@login_required
def delete_tutorship(request, pk):
    tutorship = get_object_or_404(models.Tutorship, pk=pk)
    if request.method == "POST":
        tutorship.delete()
        return HttpResponseRedirect("/tutorship")
    return HttpResponseRedirect("/tutorship")


def public_user(request, pk):
    tutor = get_object_or_404(models.CustomUser, pk=pk)
    return render(
        request,
        "profile/public.html",
        {"tutor": tutor},
    )
