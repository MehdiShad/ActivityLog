# Generated by Django 4.0.7 on 2023-10-03 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0038_learningresource_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='creator',
            old_name='created_resources_creators',
            new_name='created_resources',
        ),
    ]
