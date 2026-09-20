from datetime import datetime

from django.db import migrations
from django.utils import timezone


def fix_bem_intern_start_date(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.filter(
        title="BEM Fasilkom UI",
        role="Intern of Academic Department",
    ).update(started_at=timezone.make_aware(datetime(2025, 9, 1)))


def restore_bem_intern_start_date(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.filter(
        title="BEM Fasilkom UI",
        role="Intern of Academic Department",
    ).update(started_at=timezone.make_aware(datetime(2026, 9, 20)))


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0012_split_bem_experiences"),
    ]

    operations = [
        migrations.RunPython(
            fix_bem_intern_start_date,
            restore_bem_intern_start_date,
        ),
    ]