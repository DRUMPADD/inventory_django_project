# Generated by Django 4.1 on 2024-05-08 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_producto_no_serie_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='orden_compra',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]