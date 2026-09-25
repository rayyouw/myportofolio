from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_awards,
    show_education,
    show_skills,
    show_projects,
    show_certificates,
    create_project,
    update_project,
    create_awards,
    update_awards,
    get_projects_json,
    get_awards_json,
    get_certificates_json,
    delete_awards,
    delete_project,
    register,
    login_user,
    logout_user,
    toggle_star,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("experience/", show_experience, name="show_experience"),
    path("awards/", show_awards, name="show_awards"),
    path("awards/add/", create_awards, name="create_awards"),
    path("awards/<int:awards_id>/edit/", update_awards, name="update_awards"),
    path("awards/<int:awards_id>/delete/", delete_awards, name="delete_awards"),
    path("education/", show_education, name="show_education"),
    path("skills/", show_skills, name="show_skills"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/<int:project_id>/edit/", update_project, name="update_project"),
    path("projects/<int:project_id>/delete/", delete_project, name="delete_project"),
    path("projects/<int:project_id>/star/", toggle_star, name="toggle_star"),
    path("certificates/", show_certificates, name="show_certificates"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/awards/", get_awards_json, name="get_awards_json"),
    path("api/certificates/", get_certificates_json, name="get_certificates_json"),
]