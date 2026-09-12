from django.shortcuts import render

from main.models import (
    Award,
    Education,
    Experience,
    Profile,
    Project,
    SkillCategory,
)


def show_main(request):
    context = {
            "profile": Profile.objects.first(),
    }
    return render(request, "profile.html", context)


def show_experience(request):
    context = {
        "profile": Profile.objects.first(),
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_awards(request):
    context = {
        "profile": Profile.objects.first(),
        "award_list": Award.objects.all(),
    }
    return render(request, "awards.html", context)


def show_education(request):
    context = {
        "profile": Profile.objects.first(),
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


def show_skills(request):
    context = {
        "profile": Profile.objects.first(),
        "skill_categories": SkillCategory.objects.prefetch_related("skills"),
    }
    return render(request, "skills.html", context)


def show_projects(request):
    context = {
        "profile": Profile.objects.first(),
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)