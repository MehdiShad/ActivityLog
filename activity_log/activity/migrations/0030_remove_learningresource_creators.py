# Generated by Django 4.0.7 on 2023-10-03 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0029_activitylog_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learningresource',
            name='creators',
        ),
    ]
