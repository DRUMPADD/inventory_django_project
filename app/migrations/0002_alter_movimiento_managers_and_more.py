# Generated by Django 4.1 on 2024-05-27 19:44

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='movimiento',
            managers=[
                ('movements', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameField(
            model_name='movimiento',
            old_name='echa_regreso',
            new_name='fecha_regreso',
        ),
    ]