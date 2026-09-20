from django.db import migrations


def update_bem_experience(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.filter(title="BEM Fasilkom UI").update(
        role="Intern of Academic Department",
        highlights=[
            "Served as Person in Charge for Growto Workshop, exploring the topics of web development and data science.",
        ],
    )


def restore_bem_experience(apps, schema_editor):
    experience_model = apps.get_model("main", "Experience")
    experience_model.objects.filter(title="BEM Fasilkom UI").update(
        role="Staff of Academic Department",
        highlights=[
            "Served as Person in Charge for Sekolah BEM Fasilkom, an onboarding and educational program for new students.",
            "Supervised and evaluated interns by providing guidance and monitoring their project-based learning assignments.",
        ],
    )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0010_award_created_at"),
    ]

    operations = [
        migrations.RunPython(update_bem_experience, restore_bem_experience),
    ]