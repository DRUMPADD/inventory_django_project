# Generated by Django 4.1 on 2024-05-16 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_producto_uso_condicion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto_uso',
            name='condicion',
            field=models.TextField(blank=True, default=''),
        ),
    ]
