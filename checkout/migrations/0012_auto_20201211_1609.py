# Generated by Django 3.0.1 on 2020-12-11 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_auto_20201211_1602'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productorder',
            old_name='lineitem_total',
            new_name='product_price',
        ),
    ]
