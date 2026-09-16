from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import AccessCodeForm, AwardsForm, ProjectForm

from main.models import (
    Award,
    Education,
    Experience,
    Profile,
    Project,
    SkillCategory,
)


ACCESS_CODE = getattr(settings, "PORTFOLIO_ACCESS_CODE", "rayhanfairuz")


def has_valid_access_code(request):
    return AccessCodeForm(request.POST).is_valid() and request.POST["access_code"] == ACCESS_CODE


def show_main(request):
    context = {
            "profile": Profile.objects.first(),
    }
    return render(request, "profile.html", context)


def show_experience(request):
    experiences = Experience.objects.order_by("-started_at")
    context = {
        "profile": Profile.objects.first(),
        "professional_experiences": experiences.filter(
            title__icontains="teaching assistant",
        ),
        "organization_experiences": experiences.exclude(
            title__icontains="teaching assistant",
        ),
    }
    return render(request, "experience.html", context)


def show_awards(request):
    json_response = get_awards_json(request)
    awards = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    context = {
        "profile": Profile.objects.first(),
        "award_list": [award.object for award in awards],
    }
    return render(request, "awards.html", context)


def create_awards(request):
    form = AwardsForm(request.POST or None)
    access_form = AccessCodeForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if access_form.is_valid() and access_form.cleaned_data["access_code"] == ACCESS_CODE:
            form.save()
            messages.success(request, "Award baru berhasil ditambahkan!")
            return redirect("main:show_awards")
        access_form.add_error("access_code", "Kode akses salah.")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
        "access_form": access_form,
        "form_title": "Tambah Award",
        "form_action": "main:create_awards",
        "submit_label": "Tambah Award",
    }
    return render(request, "awards_form.html", context)


def update_awards(request, awards_id):
    award = get_object_or_404(Award, pk=awards_id)
    form = AwardsForm(request.POST or None, instance=award)
    access_form = AccessCodeForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if access_form.is_valid() and access_form.cleaned_data["access_code"] == ACCESS_CODE:
            form.save()
            messages.success(request, "Award berhasil diperbarui!")
            return redirect("main:show_awards")
        access_form.add_error("access_code", "Kode akses salah.")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
        "access_form": access_form,
        "form_title": "Edit Award",
        "form_action": "main:update_awards",
        "submit_label": "Simpan Perubahan",
        "award": award,
    }
    return render(request, "awards_form.html", context)


def get_awards_json(request):
    title_query = request.GET.get("title", "").strip()
    awards = Award.objects.all()

    if title_query:
        awards = awards.filter(title__icontains=title_query)

    awards_json = serializers.serialize("json", awards)
    return HttpResponse(awards_json, content_type="application/json")


def delete_awards(request, awards_id):
    award = get_object_or_404(Award, pk=awards_id)

    if request.method == "POST":
        if has_valid_access_code(request):
            award.delete()
            messages.success(request, "Award berhasil dihapus!")
        else:
            messages.error(request, "Kode akses salah. Award tidak dihapus.")

    return redirect("main:show_awards")


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
    json_response = get_projects_json(request)
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "profile": Profile.objects.first(),
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)
    access_form = AccessCodeForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if access_form.is_valid() and access_form.cleaned_data["access_code"] == ACCESS_CODE:
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_projects")
        access_form.add_error("access_code", "Kode akses salah.")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
        "access_form": access_form,
    }
    return render(request, "projects_form.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if has_valid_access_code(request):
            project.delete()
            messages.success(request, "Project berhasil dihapus!")
        else:
            messages.error(request, "Kode akses salah. Project tidak dihapus.")

    return redirect("main:show_projects")