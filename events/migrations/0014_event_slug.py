# Generated by Django 2.0.7 on 2019-03-12 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20190312_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(default='abc'),
        ),
    ]
