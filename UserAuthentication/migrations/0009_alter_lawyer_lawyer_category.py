# Generated by Django 4.0.2 on 2023-05-08 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LawyerManagement', '0003_paymentplan'),
        ('UserAuthentication', '0008_alter_lawyer_payment_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lawyer',
            name='lawyer_category',
            field=models.ManyToManyField(to='LawyerManagement.LawyerCategory'),
        ),
    ]
