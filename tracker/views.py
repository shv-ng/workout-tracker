from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models


# Create your views here.
def home(request: HttpRequest):
    return render(request, "home.html")


@login_required
def edit_workout_view(request: HttpRequest, pk: int):
    workout = get_object_or_404(models.Workout, id=pk, user=request.user)

    if request.method == "POST":
        form = forms.WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, "Workout updated successfully")
            return redirect("workout_history")
    else:
        form = forms.WorkoutForm(instance=workout)

    return render(request, "log_workout.html", {"form": form, "workout": workout})


@login_required
def log_workout_view(request: HttpRequest):
    if request.method == "POST":
        form = forms.WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, "Workout logged successfully")

            return redirect("workout_history")
    else:
        form = forms.WorkoutForm()
    return render(request, "log_workout.html", {"form": form})


@login_required
def workout_history(request: HttpRequest):
    workouts = models.Workout.objects.filter(user=request.user).order_by("-date")
    return render(request, "workout_history.html", {"workouts": workouts})


@login_required
def delete_workout_view(request: HttpRequest, pk: int):
    workout = get_object_or_404(models.Workout, id=pk, user=request.user)

    # Delete the workout
    _ = workout.delete()

    # Display a success message
    messages.success(request, "Workout deleted successfully")
    return redirect("workout_history")
