# Generated by Django 3.2.8 on 2022-02-20 10:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_alter_project_update_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='update_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
