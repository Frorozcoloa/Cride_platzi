# Generated by Django 3.2.9 on 2021-11-27 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0002_rename_verified_circle_is_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='circle',
            old_name='is_verified',
            new_name='verified',
        ),
    ]
