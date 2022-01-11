# Generated by Django 3.2.9 on 2021-12-07 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0010_auto_20211207_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profil',
            name='type_profil',
            field=models.CharField(choices=[('Tertiaire', 'Tertiaire'), ('Hotel', 'Hôtel'), ('Particulier', 'Particulier'), ('Fast Food', 'Fast Food'), ('Station', 'Station')], max_length=255, verbose_name='Profil'),
        ),
    ]
