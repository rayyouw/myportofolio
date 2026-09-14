from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_populate_experiences"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="experience",
            name="description",
        ),
    ]