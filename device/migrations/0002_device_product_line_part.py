# Generated by Django 3.2.13 on 2023-04-20 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('device', '0001_initial'),
        ('factory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='product_line_part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factory.productlinepart'),
        ),
    ]
