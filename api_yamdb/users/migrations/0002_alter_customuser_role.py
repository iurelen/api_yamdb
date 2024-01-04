# Generated by Django 3.2 on 2024-01-03 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('moderator', 'Moderator'), ('superuser', 'Superuser')], default='user', max_length=32),
        ),
    ]