# Generated by Django 3.2.13 on 2023-04-20 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('mac_address', models.CharField(max_length=50)),
                ('port', models.CharField(max_length=10)),
                ('position', models.IntegerField()),
                ('data', models.CharField(max_length=1050)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ErrorLine',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('code', models.IntegerField()),
                ('is_vital', models.BooleanField(default=False)),
                ('section', models.CharField(choices=[('stacker', 'stacker'), ('packaging machine', 'packaging machine')], max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='HistoryData',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('data', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='device.devicetype'),
        ),
    ]
