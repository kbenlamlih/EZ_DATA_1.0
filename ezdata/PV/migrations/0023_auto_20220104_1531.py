# Generated by Django 3.2.9 on 2022-01-04 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PV', '0022_bddbat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emisission_CO2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('territ', models.CharField(max_length=100, verbose_name="Secteurs d'activité proposés par SEIZE (utilisé)")),
                ('emission', models.PositiveIntegerField(verbose_name='Hypothèses Emissions CO2 en kg CO2/kWh\t')),
            ],
        ),
        migrations.CreateModel(
            name='EZ_DRIVE',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=1000, verbose_name='Produit')),
                ('valeur', models.PositiveIntegerField(verbose_name='Valeur')),
                ('unite', models.CharField(max_length=100, verbose_name='Unité')),
                ('invest', models.PositiveIntegerField(blank=True, null=True, verbose_name='Investissement initial en €')),
            ],
        ),
        migrations.CreateModel(
            name='Hyp_cout_mobilite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=1000, verbose_name='Produit')),
                ('valeur', models.PositiveIntegerField(verbose_name='Valeur')),
                ('unite', models.CharField(max_length=100, verbose_name='Unité')),
            ],
        ),
        migrations.AlterField(
            model_name='bddbat',
            name='cout_kWh_apres',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Coût du kWh moyen après audit'),
        ),
        migrations.AlterField(
            model_name='bddbat',
            name='gain',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Gain atteingable dans le secteur'),
        ),
    ]
