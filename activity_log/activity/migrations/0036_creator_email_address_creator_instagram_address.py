# Generated by Django 4.0.7 on 2023-10-03 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0035_creator_twitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='creator',
            name='email_address',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='creator',
            name='instagram_address',
            field=models.URLField(blank=True, null=True),
        ),
    ]
