from django import forms
from . import models


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = models.Workout
        fields = ["date", "exercise", "sets", "reps", "weight"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "exercise": forms.TextInput(
                attrs={"type": "text", "class": "form-control"}
            ),
            "sets": forms.NumberInput(
                attrs={"type": "number", "class": "form-control", "min": 1}
            ),
            "reps": forms.NumberInput(
                attrs={"type": "number", "class": "form-control", "min": 1}
            ),
            "weight": forms.NumberInput(
                attrs={"type": "number", "class": "form-control", "step": "0.1"}
            ),
        }
