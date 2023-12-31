# Generated by Django 4.0.7 on 2023-08-04 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0006_alter_activityitem_content_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitylog',
            name='spend_time',
        ),
        migrations.AddField(
            model_name='activitylog',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='amount'),
        ),
        migrations.AddField(
            model_name='activitylog',
            name='unit_of_measure',
            field=models.CharField(choices=[('page', 'صفحه'), ('minute', 'دقیقه')], default='minute', max_length=75),
        ),
    ]
