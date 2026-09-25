import datetime
import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from main.forms import AwardsForm, ProjectForm

from main.models import (
    Award,
    Certificate,
    Education,
    Experience,
    Profile,
    Project,
    SkillCategory,
)


# ---------------------------------------------------------------------------
# Role helpers
# ---------------------------------------------------------------------------

def _is_editor(user):
    """Return True if the user belongs to the 'Editor' group."""
    if not user.is_authenticated:
        return False
    return user.groups.filter(name="Editor").exists()


# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("main:login")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect(request.POST.get("next") or "main:show_main")
        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return response

    context = {
        "profile": Profile.objects.first(),
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


# ---------------------------------------------------------------------------
# Main / profile
# ---------------------------------------------------------------------------

def show_main(request):
    last_login = request.COOKIES.get("last_login", "No active login session / Cookie not found")
    context = {
        "profile": Profile.objects.first(),
        "last_login": last_login,
        "is_editor": _is_editor(request.user),
    }
    return render(request, "profile.html", context)


# ---------------------------------------------------------------------------
# Experience
# ---------------------------------------------------------------------------

def show_experience(request):
    experiences = Experience.objects.order_by("-started_at")
    context = {
        "profile": Profile.objects.first(),
        "is_editor": _is_editor(request.user),
        "professional_experiences": experiences.filter(
            title__icontains="teaching assistant",
        ),
        "organization_experiences": experiences.exclude(
            title__icontains="teaching assistant",
        ),
    }
    return render(request, "experience.html", context)


# ---------------------------------------------------------------------------
# Awards
# ---------------------------------------------------------------------------

def show_awards(request):
    awards = Award.objects.all()
    context = {
        "profile": Profile.objects.first(),
        "is_editor": _is_editor(request.user),
        "award_list": awards,
    }
    return render(request, "awards.html", context)


@login_required(login_url="/login/")
def create_awards(request):
    """Only the portfolio owner (superuser) can create awards."""
    if not request.user.is_superuser:
        raise PermissionDenied

    form = AwardsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Award baru berhasil ditambahkan!")
        return redirect("main:show_awards")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
        "form_title": "Tambah Award",
        "form_action": "main:create_awards",
        "submit_label": "Tambah Award",
    }
    return render(request, "awards_form.html", context)


@login_required(login_url="/login/")
def update_awards(request, awards_id):
    """Superuser or Editor can update awards."""
    if not (request.user.is_superuser or _is_editor(request.user)):
        raise PermissionDenied

    award = get_object_or_404(Award, pk=awards_id)
    form = AwardsForm(request.POST or None, instance=award)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Award berhasil diperbarui!")
        return redirect("main:show_awards")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
        "form_title": "Edit Award",
        "form_action": "main:update_awards",
        "submit_label": "Simpan Perubahan",
        "award": award,
    }
    return render(request, "awards_form.html", context)


@login_required(login_url="/login/")
def delete_awards(request, awards_id):
    """Only the portfolio owner (superuser) can delete awards."""
    if not request.user.is_superuser:
        raise PermissionDenied

    award = get_object_or_404(Award, pk=awards_id)

    if request.method == "POST":
        award.delete()
        messages.success(request, "Award berhasil dihapus!")

    return redirect("main:show_awards")


def get_awards_json(request):
    title_query = request.GET.get("title", "").strip()
    awards = Award.objects.all()

    if title_query:
        awards = awards.filter(title__icontains=title_query)

    awards_json = serializers.serialize("json", awards)
    return HttpResponse(awards_json, content_type="application/json")


# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------

def show_education(request):
    context = {
        "profile": Profile.objects.first(),
        "is_editor": _is_editor(request.user),
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

def show_skills(request):
    context = {
        "profile": Profile.objects.first(),
        "is_editor": _is_editor(request.user),
        "skill_categories": SkillCategory.objects.prefetch_related("skills"),
    }
    return render(request, "skills.html", context)


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

def show_projects(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    context = {
        "profile": Profile.objects.first(),
        "is_editor": _is_editor(request.user),
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "projects.html", context)


@login_required(login_url="/login/")
def create_project(request):
    """Only the portfolio owner (superuser) can create projects."""
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
        "form_title": "Tambah Proyek",
        "form_action": "main:create_project",
        "submit_label": "Tambah Proyek",
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def update_project(request, project_id):
    """Superuser or Editor can update projects."""
    if not (request.user.is_superuser or _is_editor(request.user)):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "profile": Profile.objects.first(),
        "form": form,
        "form_title": "Edit Project",
        "form_action": "main:update_project",
        "submit_label": "Simpan Perubahan",
        "project": project,
        "is_editor": _is_editor(request.user),
    }
    return render(request, "projects_form.html", context)


@login_required(login_url="/login/")
def delete_project(request, project_id):
    """Only the portfolio owner (superuser) can delete projects."""
    if not request.user.is_superuser:
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")

    return redirect("main:show_projects")


def get_projects_json(request):
    """
    Public JSON endpoint for projects.
    Returns only safe fields — excludes starred_by to prevent
    leaking user account information.
    """
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    safe_fields = [
        "id", "title", "description", "tech_stack",
        "project_url", "project_image_url", "image",
        "tags", "year", "highlights", "link", "order",
    ]

    data = []
    for project in projects:
        entry = {field: getattr(project, field) for field in safe_fields}
        entry["star_count"] = project.starred_by.count()
        data.append(entry)

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    """
    Toggle star on a project (max one star per user).
    Requires login; any authenticated user may star/unstar.
    """
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")


# ---------------------------------------------------------------------------
# Certificates
# ---------------------------------------------------------------------------

def show_certificates(request):
    certificates = Certificate.objects.all()
    context = {
        "profile": Profile.objects.first(),
        "is_editor": _is_editor(request.user),
        "award_list": list(certificates),
    }
    return render(request, "certificate.html", context)


def get_certificates_json(request):
    title_query = request.GET.get("title", "").strip()
    certificates = Certificate.objects.all()

    if title_query:
        certificates = certificates.filter(title__icontains=title_query)

    certificates_json = serializers.serialize("json", certificates)
    return HttpResponse(certificates_json, content_type="application/json")
