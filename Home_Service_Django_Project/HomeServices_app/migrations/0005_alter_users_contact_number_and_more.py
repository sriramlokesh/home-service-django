# Generated by Django 5.2.1 on 2025-05-31 11:46

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeServices_app', '0004_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='contact_number',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='workers',
            name='contact_number',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.CreateModel(
            name='ServiceTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('status_update', models.CharField(max_length=255)),
                ('battery_level', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('estimated_arrival_time', models.DateTimeField(blank=True, null=True)),
                ('signal_strength', models.IntegerField(blank=True, null=True)),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomeServices_app.response')),
            ],
            options={
                'verbose_name': 'Service Tracking',
                'verbose_name_plural': 'Service Trackings',
                'ordering': ['-created_at'],
            },
        ),
    ]
