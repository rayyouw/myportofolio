from django import forms
from django.forms import ModelForm, TextInput, Textarea, URLInput

from main.models import Project
from main.models import Award


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about your project",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class AwardsForm(ModelForm):
    class Meta:
        model = Award
        fields = [
            "title",
            "description",
            "thumbnail",
        ]

        labels = {
            "title": "Nama Lomba",
            "description": "Deskripsi Lomba",
            "thumbnail": "URL Gambar Lomba",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Data Mining - Gemastik 2026",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Tell us about your award",
                    "rows": 3,
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }


class AccessCodeForm(forms.Form):
    access_code = forms.CharField(
        label="Kode akses",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Masukkan kode akses", "autocomplete": "off"}
        ),
    )