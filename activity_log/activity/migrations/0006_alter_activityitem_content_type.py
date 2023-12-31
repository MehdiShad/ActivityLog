# Generated by Django 4.0.7 on 2023-08-04 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_rename_topics_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activityitem',
            name='content_type',
            field=models.CharField(choices=[('learning', 'Learning'), ('working', 'Working'), ('developing', 'Developing'), ('reading', 'Reading'), ('watching', 'Watching'), ('writing', 'Writing'), ('listening', 'Listening')], default='learning', max_length=110),
        ),
    ]
