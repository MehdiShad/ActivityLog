# Generated by Django 4.0.7 on 2023-10-03 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0037_rename_twitter_creator_twitter_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningresource',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
