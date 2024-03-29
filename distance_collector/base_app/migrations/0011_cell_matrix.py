# Generated by Django 3.0 on 2019-12-14 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0010_auto_20191212_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='Matrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matrix_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField()),
                ('col', models.IntegerField()),
                ('val', models.FloatField()),
                ('matrix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.Matrix')),
            ],
        ),
    ]
