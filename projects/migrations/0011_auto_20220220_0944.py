# Generated by Django 3.2.8 on 2022-02-20 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_alter_project_update_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='price',
            field=models.CharField(blank=True, default=0, max_length=200, null=True),
        ),
    ]
