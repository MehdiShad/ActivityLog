# Generated by Django 4.0.7 on 2023-08-06 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='baseuser',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='groups',
            field=models.ManyToManyField(related_name='baseuser_set_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='baseuser',
            name='user_permissions',
            field=models.ManyToManyField(related_name='baseuser_set_permissions', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.baseuser'),
        ),
    ]
