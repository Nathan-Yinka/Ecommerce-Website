# Generated by Django 4.2 on 2024-05-05 18:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0010_remove_product_primary_image_product_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productimage",
            name="primary",
        ),
    ]
