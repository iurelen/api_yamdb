# Generated by Django 3.2 on 2024-01-04 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_review_author_title_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]