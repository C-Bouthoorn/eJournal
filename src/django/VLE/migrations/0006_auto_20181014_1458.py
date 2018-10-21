# Generated by Django 2.1.2 on 2018-10-14 14:58

from django.db import migrations, models

import VLE.utils.file_handling


class Migration(migrations.Migration):

    dependencies = [
        ('VLE', '0005_presetnode_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to=VLE.utils.file_handling.get_profile_picture_path),
        ),
    ]