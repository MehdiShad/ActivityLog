# Generated by Django 4.0.7 on 2023-08-04 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_rename_github_source_activityitem_git_source'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Topics',
            new_name='Topic',
        ),
    ]
