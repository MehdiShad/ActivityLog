# Generated by Django 4.0.7 on 2023-10-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0031_learningresource_creators'),
    ]

    operations = [
        migrations.AddField(
            model_name='creator',
            name='github_address',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='creator',
            name='website_address',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='creator',
            name='youtube_address',
            field=models.URLField(blank=True, null=True),
        ),
    ]