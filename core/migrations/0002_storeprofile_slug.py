from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="storeprofile",
            name="slug",
            field=models.SlugField(blank=True, max_length=160, unique=True),
        ),
    ]
