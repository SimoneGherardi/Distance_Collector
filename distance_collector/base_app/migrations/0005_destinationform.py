# Generated by Django 3.0 on 2019-12-09 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_driverform_passengerform'),
    ]

    operations = [
        migrations.CreateModel(
            name='DestinationForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=200)),
            ],
        ),
    ]
