# Generated by Django 4.2.17 on 2025-01-11 05:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('LibData', '0005_alter_userprofile_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animeuser',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
