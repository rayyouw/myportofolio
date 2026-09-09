from datetime import datetime

from django.db import migrations
from django.db import models
from django.utils import timezone


EXPERIENCES = [
    {
        "title": "Teaching Assistant - Fasilkom UI",
        "role": "Teaching Assistant of Discrete Mathematics 1",
        "category": "part-time",
        "thumbnail": "/static/img/logo-fasilkom-ui.jpg",
        "highlights": [
            "Facilitated lesson preparation, guided students through complex discrete mathematics concepts, and evaluated academic performance through assignments and exams.",
            "Mastered propositional logic, set theory, and combinatorics while developing clear, effective, and structured academic instruction.",
        ],
        "started_at": datetime(2026, 7, 1),
        "ended_at": None,
    },
    {
        "title": "BEM Fasilkom UI",
        "role": "Staff of Academic Department",
        "category": "volunteer",
        "thumbnail": "/static/img/bem-fasilkom.png",
        "highlights": [
            "Served as Person in Charge for Sekolah BEM Fasilkom, an onboarding and educational program for new students.",
            "Supervised and evaluated interns by providing guidance and monitoring their project-based learning assignments.",
        ],
        "started_at": datetime(2026, 5, 1),
        "ended_at": None,
    },
    {
        "title": "COMPFEST 18",
        "role": "Event Associate",
        "category": "volunteer",
        "thumbnail": "/static/img/logo-compfest.png",
        "highlights": [
            "Served as Person in Charge for the Seminar and Workshop at Xcelerate Batch 2, leading concept creation and speaker and partner outreach.",
            "Coordinated Marketing, Operational, and IT Development teams to ensure seamless event execution.",
        ],
        "started_at": datetime(2026, 4, 1),
        "ended_at": None,
    },
    {
        "title": "ARUNG Fasilkom UI",
        "role": "Head of Finance",
        "category": "volunteer",
        "thumbnail": "/static/img/logo-arung.png",
        "highlights": [
            "Managed the financial responsibilities of ARUNG Fasilkom UI and supported the board's program execution.",
        ],
        "started_at": datetime(2026, 1, 1),
        "ended_at": None,
    },
    {
        "title": "Open House Fasilkom UI",
        "role": "Event Associate",
        "category": "volunteer",
        "thumbnail": "/static/img/logo-oh-2.png",
        "highlights": [
            "Served as Person in Charge for a fun coding event with 2,700+ registrants, managing participant relations and cross-team coordination.",
            "Served as Person in Charge for a parents' talk show with 100+ registrants, leading end-to-end event planning and execution.",
        ],
        "started_at": datetime(2025, 8, 1),
        "ended_at": datetime(2025, 12, 31),
    },
]


def populate_experiences(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.exclude(
        title__in=[experience["title"] for experience in EXPERIENCES]
    ).delete()

    for experience in EXPERIENCES:
        values = experience.copy()
        started_at = timezone.make_aware(values.pop("started_at"))
        ended_at = values.pop("ended_at")
        ended_at = timezone.make_aware(ended_at) if ended_at else None
        record, _ = experience_model.objects.update_or_create(
            title=values["title"],
            defaults=values,
        )
        experience_model.objects.filter(pk=record.pk).update(
            started_at=started_at,
            ended_at=ended_at,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="experience",
            name="role",
            field=models.CharField(
                blank=True,
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="experience",
            name="highlights",
            field=models.JSONField(
                blank=True,
                default=list,
            ),
        ),
        migrations.RunPython(populate_experiences, migrations.RunPython.noop),
    ]