# Generated by Django 5.0.6 on 2024-06-06 18:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_travel'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='travel',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
