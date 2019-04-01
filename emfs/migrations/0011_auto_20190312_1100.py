# Generated by Django 2.0.7 on 2019-03-12 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emfs', '0010_auto_20190312_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emf',
            name='specialty',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SP', to='events.Event'),
        ),
    ]
