# Generated by Django 4.1.7 on 2023-03-25 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoleAssignment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwithrole',
            name='picture',
            field=models.ImageField(default='media/userimg/default.png', upload_to='userimg/'),
        ),
    ]
