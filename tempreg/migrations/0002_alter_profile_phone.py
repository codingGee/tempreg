# Generated by Django 3.2.12 on 2022-04-06 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempreg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.IntegerField(default=0),
        ),
    ]