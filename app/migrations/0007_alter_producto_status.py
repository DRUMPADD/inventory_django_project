# Generated by Django 4.1.7 on 2023-11-09 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_producto_fecha_regreso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='status',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
