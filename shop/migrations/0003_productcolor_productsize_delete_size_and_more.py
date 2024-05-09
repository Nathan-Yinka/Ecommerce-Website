# Generated by Django 4.2 on 2024-05-05 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0002_remove_product_sizes_product_sizes"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductColor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Product Color",
                "verbose_name_plural": "Product Colors",
            },
        ),
        migrations.CreateModel(
            name="ProductSize",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("size", models.CharField(max_length=100)),
            ],
            options={
                "verbose_name": "Product Size",
                "verbose_name_plural": "Product Sizes",
            },
        ),
        migrations.DeleteModel(
            name="Size",
        ),
        migrations.RemoveField(
            model_name="product",
            name="colors",
        ),
        migrations.RemoveField(
            model_name="product",
            name="sizes",
        ),
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(max_length=200),
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(max_length=200),
        ),
        migrations.DeleteModel(
            name="Color",
        ),
        migrations.AddField(
            model_name="productsize",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sizes",
                to="shop.product",
            ),
        ),
        migrations.AddField(
            model_name="productcolor",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="colors",
                to="shop.product",
            ),
        ),
    ]
