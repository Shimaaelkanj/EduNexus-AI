from django import forms
from .models import Lesson

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Lesson title", "class": "input-field"}),
            "description": forms.Textarea(attrs={"placeholder": "Lesson description", "class": "textarea-field", "rows": 4}),
        }
