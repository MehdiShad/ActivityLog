# Generated by Django 4.0.7 on 2023-09-23 19:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0018_alter_activitylog_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivitySource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fa_name', models.CharField(blank=True, max_length=255, null=True)),
                ('en_name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activitylog',
            name='activity_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='activity.activitysource'),
        ),
    ]