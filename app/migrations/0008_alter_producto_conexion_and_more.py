# Generated by Django 4.1.7 on 2023-11-09 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_producto_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='conexion',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='producto',
            name='conexion_medida',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='producto',
            name='no_serie',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='producto',
            name='no_serie_interno',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
