# Generated by Django 3.0.3 on 2020-04-05 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200405_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='needs',
            field=models.TextField(blank=True, null=True),
        ),
    ]
