# Generated by Django 4.1.7 on 2023-04-27 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("EventManagement", "0002_rename_events_event"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="end_time",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="event",
            name="start_time",
            field=models.DateField(),
        ),
    ]
