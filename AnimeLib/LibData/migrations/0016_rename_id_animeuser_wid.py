# Generated by Django 4.2.17 on 2025-01-11 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LibData', '0015_remove_animeuser_uuid_alter_animeuser_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='animeuser',
            old_name='id',
            new_name='wid',
        ),
    ]
