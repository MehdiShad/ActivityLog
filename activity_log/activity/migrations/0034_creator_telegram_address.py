# Generated by Django 4.0.7 on 2023-10-03 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0033_creator_linkedin_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='creator',
            name='telegram_address',
            field=models.URLField(blank=True, null=True),
        ),
    ]
