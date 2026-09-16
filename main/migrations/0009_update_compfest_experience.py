from django.db import migrations


def update_compfest_description(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.filter(title="COMPFEST 18").update(
        highlights=[
            "Served as Person in Charge for the Seminar and Workshop at Xcelerate Batch 2, leading concept creation and partner outreach from Osnova Company.",
            "Coordinated Marketing, Operational, and IT Development teams to ensure seamless event execution.",
        ]
    )


def restore_compfest_description(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.filter(title="COMPFEST 18").update(
        highlights=[
            "Served as Person in Charge for the Seminar and Workshop at Xcelerate Batch 2, leading concept creation and speaker and partner outreach.",
            "Coordinated Marketing, Operational, and IT Development teams to ensure seamless event execution.",
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_project_description_project_project_image_url_and_more"),
    ]

    operations = [
        migrations.RunPython(
            update_compfest_description,
            restore_compfest_description,
        ),
    ]