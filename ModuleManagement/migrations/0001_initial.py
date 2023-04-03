# Generated by Django 4.1.7 on 2023-04-02 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('order', models.IntegerField(null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('order', models.IntegerField(null=True)),
                ('task_url', models.CharField(blank=True, default='', max_length=50)),
                ('view_task', models.BooleanField(default=False)),
                ('add_task', models.BooleanField(default=False)),
                ('save_task', models.BooleanField(default=False)),
                ('edit_task', models.BooleanField(default=False)),
                ('delete_task', models.BooleanField(default=False)),
                ('print_task', models.BooleanField(default=False)),
                ('cancel_task', models.BooleanField(default=False)),
                ('reset_task', models.BooleanField(default=False)),
                ('find_task', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ModuleManagement.module')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
