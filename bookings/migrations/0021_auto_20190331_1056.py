# Generated by Django 2.0.7 on 2019-03-31 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0020_detail_people'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detail',
            name='dj_entertainment',
        ),
        migrations.AddField(
            model_name='detail',
            name='DJ_Entertainment',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='detail',
            name='people',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
