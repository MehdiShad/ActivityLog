# Generated by Django 4.0.7 on 2023-08-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_activityitem_source_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='activityitem',
            name='github_source',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]