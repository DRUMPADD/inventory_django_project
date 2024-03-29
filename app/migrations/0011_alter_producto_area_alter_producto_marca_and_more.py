# Generated by Django 4.1.7 on 2023-11-13 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_producto_proveedor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='area',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='producto',
            name='marca',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='producto',
            name='modelo',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='producto',
            name='proyecto',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='producto',
            name='resguardo',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
