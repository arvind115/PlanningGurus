# Generated by Django 2.0.7 on 2019-03-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emfs', '0018_auto_20190312_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='emf',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
