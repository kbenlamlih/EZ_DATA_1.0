from django.db import models


class ModulesPV(models.Model):
    Nom = models.CharField(max_length=100)
    Puissance_modulaire_kW = models.FloatField()
    Surface_Panneau_m2 =  models.FloatField()
    Puissance_ondulaire_batterie_kW =  models.FloatField()
    Cout = models.FloatField(default = 0)

    def __str__(self):
        return self.Nom

class Onduleurs(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat')
  install= models.CharField(max_length=100, verbose_name= 'Installation  éléctrique')
  tension=  models.FloatField(verbose_name = 'Tension DC min', blank=True, null=True)
  puissance_dc =models.FloatField(verbose_name = 'Puissance DC max en kWc')
  puissance_ac = models.FloatField(verbose_name='Puissance AC max en kWc')

  def __str__(self):
      return self.model

class Monitoring(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat')
  puissance_max= models.FloatField(blank=True, null=True)

  def __str__(self):
      return self.model

#Penser a ajouter les unités
class Main_doeuvre(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat')

  def __str__(self):
      return self.model


class Tableaux(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat')

  def __str__(self):
      return self.model


class Cables(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat + installation en €/ml')

  def __str__(self):
      return self.model

class Cheminement(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat + installation en €/ml')

  def __str__(self):
      return self.model

class Divers(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat')

  def __str__(self):
      return self.model

class Inge(models.Model):
  model= models.CharField(max_length=100)
  nom_francais= models.CharField(max_length=100, blank=True)
  nom_anglais= models.CharField(max_length=100, blank=True)
  cout=models.FloatField(verbose_name = 'Coût dachat en €')

  def __str__(self):
      return self.model

class Structure(models.Model):
    model = models.CharField(max_length=100)
    nom_francais = models.CharField(max_length=100, blank=True)
    nom_anglais = models.CharField(max_length=100, blank=True)
    cout = models.FloatField(verbose_name='Coût dachat en €/Wc')

    def __str__(self):
          return self.model

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

    def __str__(self):
        return self.N

    def get_field(model):
        return model._meta.fields



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
        ('Agriculture', 'Agriculture'),
        ('Activités de bureaux', 'Activités de bureaux'),
        ('Grande distribution alimentaire', 'Grande distribution alimentaire'),
        ('Petit et moyen commerce alimentaire', 'Petit et moyen commerce alimentaire'),
        ('Commerce non alimentaire', 'Commerce non alimentaire'),
        ('Métiers de bouche', 'Métiers de bouche'),
        ('Cafés Hôtels Restaurants', 'Cafés Hôtels Restaurants'),
        ('Industrie', 'Industrie'),
        ('BTP', 'BTP'),
        ('Coiffeur, beauté, esthéticienne', 'Coiffeur, beauté, esthéticienne'),
        ('Mécanique automobile, 2 roues, vélo', 'Mécanique automobile, 2 roues, vélo'),
        ('Santé(Clinique, laboratoire, pharmacie)', 'Santé(Clinique, laboratoire, pharmacie)'),
        ('Agences bancaires', 'Agences bancaires'),
        ('Telecom(Data Center)', 'Telecom(Data Center)'),
        ('Autre', 'Autre'),
    ]
    type_batiment= models.CharField(verbose_name='Type de Bâtiment', choices=type_b, max_length= 255)
    nb_batiment = models.PositiveIntegerField(verbose_name='Nombre de bâtiments de ce type')
    nb_etages=  models.PositiveIntegerField(verbose_name="Nombre d'étage" )


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

    type = (('Terrasse', 'Terrasse'),
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

class Mobilite(models.Model):
    vehicule_fonction= models.PositiveIntegerField(verbose_name='Nombre de véhicules de fonction')
    km_an_vehicule_fonction= models.PositiveIntegerField(verbose_name='Nombre de km/an véhicule de fonction')
    vehicule_utilitaire= models.PositiveIntegerField(verbose_name='Nombre de véhicules utilitaires')
    km_an_vehicule_utilitaire= models.PositiveIntegerField(verbose_name='Nombre de km/an véhicule utilitaires')
    choix = ( ('Oui','Oui '),
            ('Non','Non '))
    parking = models.CharField(verbose_name= 'Présence parking ', choices=choix, max_length= 255)
    choix1 = (('Public', 'Public '),
             ('Privé', 'Privé '))
    acces = models.CharField(verbose_name= 'Accessibilité Parking', choices=choix1, max_length= 255)
    borne = models.CharField(verbose_name= 'Option Borne', choices=choix, max_length= 255)
    pt_de_charge= models.PositiveIntegerField(verbose_name='Nombre de point de charges desirés')

    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='batiment_mobilite', blank=True)




class Taxe(models.Model):
    territ = models.CharField(max_length=100, verbose_name='Territoire')
    transport_1= models.FloatField(verbose_name='Main doeuvre en %')
    transport_2= models.FloatField(verbose_name='Panneaux en %')
    transport_3= models.FloatField(verbose_name='Le reste en %')
    Pose_PV_toiture_tole= models.FloatField(verbose_name=' Pose PV toiture tôle + Raccordement < 50kWc')
    Pose_PV_toiture_tole_2= models.FloatField(verbose_name='Pose PV toiture tôle + Raccordement > 50kWc')
    Pose_PV_toiture_terrasse= models.FloatField(verbose_name='Pose PV toiture Terrasse + Raccordement < 50kWc')
    Pose_PV_toiture_terrasse_2= models.FloatField(verbose_name=' Pose PV toiture Terrasse + Raccordement > 50kWc')
    Pose_PV_toiture_tuile = models.FloatField(verbose_name=' Pose PV toiture Tuiles +Raccordement < 10kWc')
    Pose_PV_toiture_tuile_2= models.FloatField(verbose_name=' Pose PV toiture Tuiles +Raccordement < 50kWc')
    Pose_PV_toiture_tole_3 = models.FloatField(verbose_name='  Pose PV toiture Tuiles +Raccordement > 50kWc')
    pose = models.FloatField(verbose_name=' Pose plot soprasolar ')
    install = models.FloatField(verbose_name=' Installation et mise en service borne')
    tva_entreprise =  models.FloatField()
    tva_particulier =  models.FloatField()

    def __str__(self):
        return self.territ



class Factu_batiment(models.Model):
    batiment = models.ForeignKey(Batiment, on_delete=models.CASCADE, related_name='batiment_factu', blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='Client_factu', blank=True)
    class Meta:
        abstract=True

class Modules_factu(models.Model):
    module = models.CharField(max_length=100)
    qt = models.PositiveIntegerField(verbose_name='Quantité')
    cout_unitaire= models.PositiveIntegerField(verbose_name='Coût HA unitaire')
    cout_unitaire_transport = models.PositiveIntegerField(verbose_name='Coût Unitaire Transport', blank=True)
    predef = models.PositiveIntegerField(verbose_name='Prix unitaire prédéfini ',blank=True, null=True)
    cout_total = models.PositiveIntegerField(verbose_name='Coût Total HA')
    cout_total_transport = models.PositiveIntegerField(verbose_name='Coût Total Transport',  blank=True)
    marge = models.PositiveIntegerField()
    prix=models.PositiveIntegerField()
    prix_unitaire=models.PositiveIntegerField()

    def get_all_fields(self):
        """Returns a list of all field names on the instance."""
        fields = []
        for f in self._meta.fields:
            print(f)

            fname = f.name
            print(fname)

            # resolve picklists/choices, with get_xyz_display() function
            get_choice = 'get_' + fname + '_display'
            if hasattr(self, get_choice):
                value = getattr(self, get_choice)()
            else:
                try:
                    value = getattr(self, fname)
                except AttributeError:
                    value = None
            print(value)
            # only display fields with values and skip some fields entirely
            if f.editable and f.name not in ('id'):
                if fname not in ('module', 'predef'):
                    value= round(value, 2)
                else:
                    value = value
                if value ==None:
                    value= ''
                fields.append(
                    {
                        'label': f.verbose_name,
                        'name': f.name,
                        'value':value
                    }
                )

        return fields

class BDDBat(models.Model):
    type= models.CharField(max_length=100, verbose_name="Secteurs d'activité proposés par SEIZE (utilisé)" )
    moy_kWh_avant = models.FloatField(verbose_name="Moyenne par Secteur (kWh/an/m²) AVANT AUDIT ")
    moy_kWh_apres=  models.FloatField(verbose_name="Moyenne par Secteur (kWh/an/m²) APRES AUDIT")
    moy_euros_avant=  models.FloatField(verbose_name="Moyenne par Secteur (€/an/m²) AVANT AUDIT ")
    moy_euros_apres=  models.FloatField(verbose_name="Moyenne par Secteur (€/an/m²) APRES AUDIT")
    cout_kWh_avant= models.FloatField(verbose_name="Coût du kWh moyen avant audit")
    cout_kWh_apres = models.FloatField(verbose_name="Coût du kWh moyen après audit", blank=True, null=True)
    gain=  models.FloatField(verbose_name="Gain atteingable dans le secteur", blank=True, null=True)

    def __str__(self):
        return self.type

class Emisission_CO2(models.Model):
    territ= models.CharField(max_length=100, verbose_name="Territoire" )
    emission= models.FloatField(verbose_name="Hypothèses Emissions CO2 en kg CO2/kWh	")

class Hyp_cout_mobilite(models.Model):
    model= models.CharField(max_length=1000, verbose_name="Produit" )
    valeur= models.FloatField(verbose_name="Valeur")
    unite=  models.CharField(max_length=100, verbose_name="Unité")


class EZ_DRIVE(models.Model):
    model = models.CharField(max_length=1000, verbose_name="Produit")
    valeur = models.FloatField(verbose_name="Valeur")
    unite = models.CharField(max_length=100, verbose_name="Unité")
    invest= models.FloatField(verbose_name="Investissement initial en €", blank= True, null=True)


















