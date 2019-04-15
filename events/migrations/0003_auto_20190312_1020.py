# Generated by Django 2.0.7 on 2019-03-12 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emfs', '0007_auto_20190312_1013'),
        ('events', '0002_auto_20190312_1017'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='emf',
        ),
        migrations.AddField(
            model_name='event',
            name='emf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='emfs.Emf'),
        ),
    ]