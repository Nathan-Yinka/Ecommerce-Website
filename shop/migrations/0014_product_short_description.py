# Generated by Django 4.2 on 2024-05-12 06:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0013_product_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="short_description",
            field=models.CharField(
                default="this is the product short description",
                help_text="Short description for the product",
                max_length=200,
            ),
            preserve_default=False,
        ),
    ]
