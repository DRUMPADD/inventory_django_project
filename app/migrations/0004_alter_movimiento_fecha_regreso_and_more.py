# Generated by Django 4.1 on 2024-05-29 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_movimiento_estado_alter_movimiento_fecha_regreso_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='fecha_regreso',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='fecha_salida',
            field=models.DateField(blank=True, null=True),
        ),
    ]