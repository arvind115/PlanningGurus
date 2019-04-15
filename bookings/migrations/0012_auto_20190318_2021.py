# Generated by Django 2.0.7 on 2019-03-18 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0011_booking_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities.City'),
        ),
    ]