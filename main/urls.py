from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_awards,
    show_education,
    show_skills,
    show_projects,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("awards/", show_awards, name="show_awards"),
    path("education/", show_education, name="show_education"),
    path("skills/", show_skills, name="show_skills"),
    path("projects/", show_projects, name="show_projects"),
]