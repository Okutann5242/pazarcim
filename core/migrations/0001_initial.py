# Generated manually
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StoreProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("store_name", models.CharField(default="Mağazam", max_length=150)),
                ("description", models.TextField(blank=True)),
                ("support_email", models.EmailField(blank=True, max_length=254)),
                ("support_phone", models.CharField(blank=True, max_length=40)),
                ("logo", models.ImageField(blank=True, null=True, upload_to="store/logo/")),
                ("banner", models.ImageField(blank=True, null=True, upload_to="store/banner/")),
                ("owner", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="store_profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "Dükkan Profili", "verbose_name_plural": "Dükkan Profilleri"},
        ),
        migrations.CreateModel(
            name="DiscountCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=40, unique=True)),
                ("percent", models.PositiveIntegerField(help_text="0-100 arası indirim yüzdesi")),
                ("is_active", models.BooleanField(default=True)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="IntegrationSetting",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("key", models.CharField(max_length=80, unique=True)),
                ("value", models.TextField(blank=True)),
                ("is_enabled", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Payout",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(max_length=120, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("note", models.CharField(blank=True, max_length=255)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="RefundRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order_id", models.PositiveIntegerField()),
                ("customer_email", models.EmailField(blank=True, max_length=254)),
                ("reason", models.TextField()),
                ("status", models.CharField(choices=[("open", "Açık"), ("approved", "Onaylandı"), ("rejected", "Reddedildi"), ("closed", "Kapandı")], default="open", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ShippingMethod",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("flat_fee", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="VariationType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="VariationOption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60)),
                ("variation_type", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="options", to="core.variationtype")),
            ],
            options={"unique_together": {("variation_type", "name")}},
        ),
    ]
