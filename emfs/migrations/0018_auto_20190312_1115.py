# Generated by Django 2.0.7 on 2019-03-12 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_remove_event_emf'),
        ('emfs', '0017_auto_20190312_1109'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emf',
            name='event',
        ),
        migrations.RemoveField(
            model_name='emf',
            name='events_handled',
        ),
        migrations.RemoveField(
            model_name='emf',
            name='events',
        ),
        migrations.AddField(
            model_name='emf',
            name='events',
            field=models.ManyToManyField(blank=True, to='events.Event'),
        ),
    ]