# Generated by Django 4.1 on 2024-05-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_producto_orden_compra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='tamanio',
            field=models.CharField(blank=True, default=0, max_length=20),
        ),
    ]
