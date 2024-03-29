# Generated by Django 3.0 on 2019-12-09 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0003_passenger_starting_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('starting_point', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PassengerForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('starting_point', models.CharField(max_length=100)),
            ],
        ),
    ]
