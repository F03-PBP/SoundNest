# Generated by Django 5.1.2 on 2024-10-26 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BestDeals', '0004_delete_userinteraction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='sale_start_time',
        ),
    ]
