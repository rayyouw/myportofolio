from django.db import migrations


def fix_study_program(apps, schema_editor):
    Profile = apps.get_model("main", "Profile")
    Profile.objects.all().update(study_program="Computer Science")


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0016_fix_study_program"),
    ]

    operations = [
        migrations.RunPython(fix_study_program, migrations.RunPython.noop),
    ]
