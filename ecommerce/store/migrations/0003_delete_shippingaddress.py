# Generated by Django 5.0.4 on 2024-04-30 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_product_image"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ShippingAddress",
        ),
    ]