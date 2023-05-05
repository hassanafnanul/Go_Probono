# Generated by Django 4.1.7 on 2023-05-03 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Zone",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("slug", models.CharField(max_length=100)),
                (
                    "zone_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("division", "Division"),
                            ("city", "City"),
                            ("area", "Area"),
                        ],
                        default="area",
                        max_length=9,
                    ),
                ),
                (
                    "parent_slug",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("extra_info", models.CharField(max_length=100, null=True)),
                ("is_archived", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="Appoinment.zone",
                    ),
                ),
            ],
        ),
    ]
