# Generated by Django 2.0.7 on 2019-03-31 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0017_booking_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detail',
            name='decor',
            field=models.CharField(blank=True, choices=[('floral', 'Floral'), ('sober', 'Sober'), ('premium', 'Premium'), ('artificial', 'Artificial')], max_length=40, null=True),
        ),
    ]
