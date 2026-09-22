from django.db import migrations


def fix_study_program(apps, schema_editor):
    Profile = apps.get_model("main", "Profile")
    Profile.objects.filter(study_program__iexact="ilmu komputer").update(
        study_program="Computer Science"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0015_profile_username"),
    ]

    operations = [
        migrations.RunPython(fix_study_program, migrations.RunPython.noop),
    ]
