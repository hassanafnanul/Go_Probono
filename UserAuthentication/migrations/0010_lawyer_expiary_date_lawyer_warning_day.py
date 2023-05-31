# Generated by Django 4.1.7 on 2023-05-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("UserAuthentication", "0009_alter_lawyer_lawyer_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="lawyer",
            name="expiary_date",
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="lawyer",
            name="warning_day",
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
    ]
