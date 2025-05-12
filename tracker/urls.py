from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("workout/log", views.log_workout_view, name="log_workout"),
    path("workout/history/", views.workout_history, name="workout_history"),
    path("workouts/delete/<int:pk>/", views.delete_workout_view, name="delete_workout"),
    path("workout/edit/<int:pk>/", views.edit_workout_view, name="edit_workout"),
]
