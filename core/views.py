from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
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
    if tutorship.tutor != request.user:
        raise Http404("You are not authorized to edit this review.")
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
    if tutorship.tutor != request.user:
        raise Http404("You are not authorized to edit this review.")
    if request.method == "POST":
        tutorship.delete()
        return HttpResponseRedirect("/tutorship")
    return HttpResponseRedirect("/tutorship")


@login_required
def public_user(request, pk):
    tutor = get_object_or_404(models.CustomUser, pk=pk)

    reviews = models.Review.objects.filter(reviewed=tutor).order_by("-created_at")
    paginator = Paginator(reviews, 5)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "profile/public.html",
        {"tutor": tutor, "page_obj": page_obj},
    )


@login_required
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

            previous_page_url = request.META.get("HTTP_REFERER")
            fallback_url = reverse("tutorship")
            return redirect(previous_page_url or fallback_url)
    else:
        form = forms.ReviewForm()
    return render(request, "review/create.html", {"form": form, "tutor": reviewed})


@login_required
def edit_review(request, pk):
    review_to_edit = get_object_or_404(models.Review, pk=pk)
    if review_to_edit.author != request.user:
        raise Http404("You are not authorized to edit this review.")
    previous_page = request.META.get("HTTP_REFERER") or reverse("home")

    if request.method == "POST":
        form = forms.ReviewForm(request.POST)

        if form.is_valid():
            review_to_edit.body = form.cleaned_data["body"]
            review_to_edit.rating = form.cleaned_data["rating"]
            review_to_edit.save()
            return redirect(previous_page)
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
def delete_review(request, pk):
    review = get_object_or_404(models.Review, pk=pk)
    if review.author != request.user:
        raise Http404("You are not authorized to edit this review.")
    if request.method == "POST":
        review.delete()
        return HttpResponseRedirect("/tutorship")
    return HttpResponseRedirect("/tutorship")
