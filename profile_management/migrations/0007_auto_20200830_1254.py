# Generated by Django 3.1 on 2020-08-30 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_management', '0006_auto_20200830_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
