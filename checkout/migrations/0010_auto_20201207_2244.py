# Generated by Django 3.0.1 on 2020-12-07 22:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_auto_20201207_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of order'),
        ),
    ]
