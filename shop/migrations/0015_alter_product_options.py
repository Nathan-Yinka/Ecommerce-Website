# Generated by Django 4.2 on 2024-05-14 12:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0014_product_short_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["-created", "-updated", "-id"]},
        ),
    ]