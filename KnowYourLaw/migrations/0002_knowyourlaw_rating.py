# Generated by Django 4.1.7 on 2023-03-26 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KnowYourLaw', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowyourlaw',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
