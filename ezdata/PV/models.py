from django.db import models


class ModulesPV(models.Model):
    Nom = models.CharField(max_length=100)
    Puissance_modulaire_kW = models.FloatField()
    Surface_Panneau_m2 =  models.FloatField()
    Puissance_ondulaire_batterie_kW =  models.FloatField()

    def __str__(self):
        return self.Nom
# Create your models here.

class BDD(models.Model):
    N = models.FloatField(null=True)
    Onduleur_1= models.CharField(max_length=100, null=True)
    Batterie_1= models.CharField(max_length=100, blank=True, null=True)
    Nombre_Batterie_1= models.FloatField(blank=True, null=True)
    Onduleur_2= models.CharField(max_length=100, blank=True, null=True)
    Batterie_2= models.CharField(max_length=100, blank=True, null=True)
    Nombre_Batterie_2= models.PositiveIntegerField(blank=True, null=True)
    Onduleur_3= models.CharField(max_length=100, blank=True, null=True)
    Module_batterie_1= models.CharField(max_length=100, blank=True, null=True)
    Module_batterie_2= models.CharField(max_length=100, blank=True, null=True)
    Electrical_installation = models.CharField(max_length=100, null=True)
    Nb_modules_min = models.FloatField(null=True)
    Puissance_centrale_max= models.FloatField(null=True)
    Capacit_batterie = models.FloatField(null=True)
    Prix_total_achat= models.FloatField(null=True)

    #def __str__(self):
        #return self.N


class Client(models.Model):
    nom_entreprise = models.CharField(verbose_name = 'Nom Entreprise', max_length= 255)
    mail = models.EmailField(verbose_name='E-mail')
    enseigne = models.ForeignKey('Enseigne', on_delete=models.CASCADE, related_name='Enseigne_client', blank=True, null=True)

    def __str__(self):
        return self.nom_entreprise


class Enseigne(models.Model):
    secteur = models.CharField(verbose_name ='Secteur', max_length= 255)
    nb_sites = models.PositiveIntegerField(verbose_name='Nombre de sites')
    effectif = models.PositiveIntegerField(verbose_name='Effectif')

    id = models.AutoField(primary_key=True, editable=False,  blank=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE,related_name='Client_Enseigne', blank = True)
    batiment = models.ForeignKey('Batiment', on_delete=models.CASCADE, related_name='Batiment_id_client', blank=True, null=True)


    def __str__(self):
        return self.secteur

class Batiment(models.Model):

    type_b = [
        ('AG', 'Agriculture'),
        ('AB', 'Activités de bureaux'),
        ('GA', 'Grande distribution alimentaire'),
        ('PMA', 'Petit et moyen commerce alimentaire'),
        ('CNA', 'Commerce non alimentaire'),
        ('MB', 'Métiers de bouche'),
        ('CHR', 'Cafés Hôtels Restaurants'),
        ('I', 'Industrie'),
        ('BTP', 'BTP'),
        ('CBE', 'Coiffeur, beauté, esthéticienne'),
        ('M', 'Mécanique automobile, 2 roues, vélo'),
        ('S', 'Santé(Clinique, laboratoire, pharmacie)'),
        ('AB', 'Agences bancaires'),
        ('T', 'Telecom(Data Center)'),
        ('A', 'Autre'),
    ]
    type_batiment= models.CharField(verbose_name='Type de Bâtiment', choices=type_b, max_length= 255)
    nb_batiment = models.PositiveIntegerField(verbose_name='Nombre de bâtiments de ce type')

    categ = [
        ('Petit', 'Petit (< 150m²)'),
        ('Moyen', 'Moyen (150-500m²)'),
        ('Grand', 'Grand (500m²-1000m²)'),
        ('Tres grand', 'Très grand (> 1000m²)'),
    ]

    taille = models.CharField(verbose_name='Taille',choices=categ, max_length= 255)
    enseigne= models.ForeignKey('Enseigne', on_delete=models.CASCADE, related_name='Enseigne_batiment', blank=True)
    localisation = models.ForeignKey('Localisation', on_delete=models.CASCADE,  related_name='Localisation_batiment', blank=True, null=True)
    profil = models.ForeignKey('Profil', on_delete=models.CASCADE,related_name='Profil_batiment',blank=True, null=True)
    toiture = models.ForeignKey('Toiture',  on_delete=models.CASCADE,related_name='Toiture_batiment', blank=True, null=True)
    edf = models.ForeignKey('EDF', on_delete=models.CASCADE,related_name='edf_batiment',blank=True, null=True)




    id = models.AutoField(primary_key=True, editable=False,  blank=True)

    def __str__(self):
        return self.type_batiment

class Localisation(models.Model):
    territ = models.CharField(verbose_name = 'Territoire', max_length= 255)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE,related_name='Batiment_localisation', blank=True)

    def __str__(self):
        return self.territ



class Profil (models.Model):
    profil = [
        ('Tertiaire', 'Tertiaire'),
        ('Hotel', 'Hôtel'),
        ('Particulier', 'Particulier'),
        ('Fast Food', 'Fast Food'),
        ('Station', 'Station'),
    ]

    type_profil = models.CharField(verbose_name = 'Profil',choices=profil, max_length= 255)
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='batiment_profil', blank=True)

    def __str__(self):
        return self.profil



class Toiture(models.Model):

    type = (('Tôle', 'Tôle'),
        ('Tôle bac acier trapézoïdal','Tôle bac acier trapézoïdal'),
    )

    toiture = models.CharField(verbose_name= 'Toiture', choices=type, max_length= 255)
    surface = models.PositiveIntegerField(verbose_name='Surface de toiture')

    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='batiment_toiture', blank=True)

    def __str__(self):
        return self.toiture


class EDF(models.Model):
    puissance = models.PositiveIntegerField(verbose_name='Puissance souscrite')

    ref = ( ('Mensuelle','Mensuelle '),
            ('Bimestrielle','Bimestrielle '),
            ('Annuelle','Annuelle '))

    reference = models.CharField(verbose_name= 'Reference', choices=ref, max_length= 255)

    nb_kW = models.PositiveIntegerField(verbose_name='Nombre KWh facture')

    facture = models.PositiveIntegerField(verbose_name='Montant facture ')
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE,related_name='batiment_edf',  blank=True)
    electrification = models.ForeignKey('Electrification', on_delete=models.CASCADE,related_name='souscription_batiment', blank=True, null=True)

    id = models.AutoField(primary_key=True, editable=False)



    def __str__(self):
        return self.nb_kW

class Electrification(models.Model):
    instal = ( ('Monophasée','Monophasée'),
                ('Triphasée','Triphasée'),)
    installation = models.CharField(verbose_name= 'Installation', choices=instal, max_length= 255)
    souscription = models.ForeignKey(EDF, on_delete=models.CASCADE, related_name='batiment_souscription', blank=True)

    def __str__(self):
        return self.instal










