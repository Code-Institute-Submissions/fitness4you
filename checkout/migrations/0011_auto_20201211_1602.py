# Generated by Django 3.0.1 on 2020-12-11 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_auto_20201207_2244'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productorder',
            old_name='product_price',
            new_name='lineitem_total',
        ),
    ]