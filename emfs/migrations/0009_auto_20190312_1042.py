# Generated by Django 2.0.7 on 2019-03-12 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_remove_event_emf'),
        ('emfs', '0008_emf_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emf',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='emf',
            name='email',
            field=models.EmailField(blank=True, max_length=50, unique=True),
        ),
        migrations.RemoveField(
            model_name='emf',
            name='event',
        ),
        migrations.AddField(
            model_name='emf',
            name='event',
            field=models.ManyToManyField(blank=True, null=True, to='events.Event'),
        ),
        migrations.AlterField(
            model_name='emf',
            name='events_handled',
            field=models.CharField(choices=[('birthday', 'Birthday'), ('wedding', 'Wedding'), ('dwedding', 'DWedding'), ('anniversary', 'Anniversary'), ('festive', 'Festive'), ('special', 'Special'), ('corporate', 'Corporate')], default='Birthday', max_length=2),
        ),
        migrations.AlterField(
            model_name='emf',
            name='region',
            field=models.CharField(max_length=50),
        ),
    ]