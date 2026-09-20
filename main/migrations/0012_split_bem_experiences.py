from datetime import datetime

from django.db import migrations
from django.utils import timezone


def split_bem_experiences(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    staff_experience = experience_model.objects.filter(
        title="BEM Fasilkom UI",
    ).order_by("started_at", "id").first()

    if staff_experience:
        staff_experience.role = "Staff of Academic Department"
        staff_experience.highlights = [
            "Served as Person in Charge for Sekolah BEM Fasilkom, an onboarding and educational program for new students.",
            "Supervised and evaluated interns by providing guidance and monitoring their project-based learning assignments.",
        ]
        staff_experience.save(update_fields=["role", "highlights"])

    experience_model.objects.create(
        title="BEM Fasilkom UI",
        role="Intern of Academic Department",
        category="volunteer",
        thumbnail="/static/img/bem-fasilkom.png",
        highlights=[
            "Served as Person in Charge for Growto Workshop, exploring the topics of web development and data science.",
        ],
        started_at=timezone.make_aware(datetime(2025, 9, 1)),
        ended_at=timezone.make_aware(datetime(2025, 11, 30)),
    )


def restore_bem_experiences(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.filter(
        title="BEM Fasilkom UI",
        role="Intern of Academic Department",
        started_at=timezone.make_aware(datetime(2025, 9, 1)),
        ended_at=timezone.make_aware(datetime(2025, 11, 30)),
    ).delete()

    experience_model.objects.filter(title="BEM Fasilkom UI").update(
        role="Intern of Academic Department",
        highlights=[
            "Served as Person in Charge for Growto Workshop, exploring the topics of web development and data science.",
        ],
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0011_update_bem_experience"),
    ]

    operations = [
        migrations.RunPython(split_bem_experiences, restore_bem_experiences),
    ]