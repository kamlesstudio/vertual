# Generated by Django 3.2.8 on 2022-02-19 22:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_update_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='update_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 2, 19, 22, 17, 56, 505168, tzinfo=utc), null=True),
        ),
    ]
