# Generated by Django 3.2.9 on 2022-01-03 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0020_auto_20211229_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modules_factu',
            name='batiment',
        ),
        migrations.RemoveField(
            model_name='modules_factu',
            name='client',
        ),
    ]
