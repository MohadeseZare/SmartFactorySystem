# Generated by Django 4.0.4 on 2023-04-04 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('factory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='factorymember',
            name='product_line_id',
        ),
        migrations.AddField(
            model_name='factorymember',
            name='product_line',
            field=models.ManyToManyField(blank=True, default=[], to='factory.productline'),
        ),
        migrations.AlterField(
            model_name='factory',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='factorymember',
            name='factory',
            field=models.ManyToManyField(blank=True, default=[], to='factory.factory'),
        ),
        migrations.AlterField(
            model_name='factorymember',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='factory',
            unique_together={('id', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='productline',
            unique_together={('id', 'name')},
        ),
    ]
