# Generated by Django 4.2 on 2024-05-05 18:35

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0007_alter_productimage_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image",
            field=models.ImageField(
                default="dff", upload_to=shop.models.product_image_upload_path
            ),
            preserve_default=False,
        ),
    ]
