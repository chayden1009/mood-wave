# Generated by Django 5.0.1 on 2024-01-21 05:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_mood_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mood',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]