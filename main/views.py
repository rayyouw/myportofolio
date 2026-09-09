from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Rayhan Fairuz Aqram",
        "npm": "2506586186",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "A Computer Science student at Universitas Indonesia interested "
            "in data science and artificial intelligence."
        ),
        "experience_list": Experience.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rayhan Fairuz Aqram",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)