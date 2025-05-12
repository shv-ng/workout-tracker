from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpRequest
from django.shortcuts import redirect, render

from tracker import models as tracker_models

from . import forms

# Create your views here.


def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        print(form)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("home")
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "login.html", context=context)


def register_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = forms.RegistrationForm()
    context = {"form": form}
    return render(request, "register.html", context=context)


@login_required
def logout_view(request: HttpRequest):
    logout(request)
    return redirect("home")


@login_required
def profile_view(request: HttpRequest):
    workouts = tracker_models.Workout.objects.filter(user=request.user).order_by(
        "-date"
    )
    return render(
        request,
        "profile.html",
        {
            "user": request.user,
            "workouts": workouts,
        },
    )


@login_required
def edit_profile_view(request: HttpRequest):
    if request.method == "POST":
        form = forms.EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        form = forms.EditProfileForm(instance=request.user)
    return render(request, "edit_profile.html", {"form": form})


@login_required
def change_password_view(request: HttpRequest):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password changed successfully.")
            return redirect("profile")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


@login_required
def delete_account_view(request: HttpRequest):
    if request.method == "POST":
        _ = request.user.delete()
        messages.success(request, "Account deleted successfully.")
        return redirect("home")
    return render(request, "delete_account.html")
