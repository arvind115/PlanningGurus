# Generated by Django 2.0.7 on 2019-03-14 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emfs', '0020_auto_20190313_2259'),
        ('bookings', '0004_auto_20190314_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='emf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emfs.Emf'),
        ),
    ]
