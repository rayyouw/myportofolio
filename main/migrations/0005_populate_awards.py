from django.db import migrations


AWARDS = [
    {
        "title": "Data Mining - GEMASTIK 2026",
        "description": "Finalist at National Level",
        "thumbnail": "/static/img/logo-gemastik.png",
    },
    {
        "title": "Big Data Challenge - SATRIA DATA 2026",
        "description": "Representative of Universitas Indonesia",
        "thumbnail": "/static/img/logo-satria-data.jpg",
    },
    {
        "title": "National Olympiad in Informatics (OSN Informatika) 2024",
        "description": "Silver Medal at Provincial Level",
        "thumbnail": "/static/img/logo-osn.png",
    },
    {
        "title": "National Olympiad in Informatics (OSN Informatika) 2023",
        "description": "Silver Medal at Provincial Level",
        "thumbnail": "/static/img/logo-osn.png",
    },
    {
        "title": "National Olympiad in Mathematics (OSN Matematika) 2018",
        "description": "Finalist at National Level",
        "thumbnail": "/static/img/logo-osn.png",
    },
]


def populate_awards(apps, schema_editor):
    award_model = apps.get_model("main", "Award")
    for award in AWARDS:
        award_model.objects.update_or_create(
            title=award["title"],
            defaults=award,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_award"),
    ]

    operations = [
        migrations.RunPython(populate_awards, migrations.RunPython.noop),
    ]
