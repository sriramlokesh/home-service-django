# Generated by Django 4.2 on 2025-06-21 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeServices_app', '0012_alter_adminregistrationrequest_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminregistrationrequest',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
