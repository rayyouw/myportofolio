from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_awards,
    show_education,
    show_skills,
    show_projects,
    create_project,
    create_awards,
    update_awards,
    get_projects_json,
    get_awards_json,
    delete_awards,
    delete_project,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("awards/", show_awards, name="show_awards"),
    path("awards/add/", create_awards, name="create_awards"),
    path("awards/<int:awards_id>/edit/", update_awards, name="update_awards"),
    path("awards/<int:awards_id>/delete/", delete_awards, name="delete_awards"),
    path("education/", show_education, name="show_education"),
    path("skills/", show_skills, name="show_skills"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/awards/", get_awards_json, name="get_awards_json"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
]