# Generated by Django 3.2.13 on 2024-01-27 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('factory', '0001_initial'),
        ('device', '0003_alter_device_product_line_part'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='product_line_part',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factory.productlinepart'),
        ),
    ]
