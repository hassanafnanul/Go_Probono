# Generated by Django 4.1.7 on 2023-03-14 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAuthentication', '0002_customer_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='latitude',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='longitude',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
