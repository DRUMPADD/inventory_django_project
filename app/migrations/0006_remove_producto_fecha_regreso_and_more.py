# Generated by Django 4.1.7 on 2023-11-08 19:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_producto_libraje_alter_producto_tamanio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='fecha_regreso',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='fecha_salida',
        ),
        migrations.AlterField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='app.proveedor'),
        ),
    ]
