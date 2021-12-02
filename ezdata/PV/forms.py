from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _



class Client(forms.Form):
    nom_entreprise = forms.CharField(initial = 'Nom Entreprise',
                                     widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Green Technologie'}))
    territ = forms.CharField(initial = 'Territoire' ,
                             widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Martinique'}))
    mail= forms.EmailField(initial= 'E-mail',
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'kenza.benlamlih@greentechnologie.net'}))
    secteur = forms.CharField(initial ='Secteur',
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Services'}))
    nb_sites = forms.IntegerField(initial = 'Nombre de sites',
                                          widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30'}))
    effectif = forms.IntegerField(initial = 'Effectif',
                                          widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '150'}))


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
    type_batiment= forms.MultipleChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                              choices=type_b)

    profil = [
        ('tertiaire', 'Tertiaire'),
        ('hotel', 'Hôtel'),
        ('particulier', 'Particulier'),
        ('fast_food', 'Fast Food'),
        ('station', 'Station'),
    ]

    ##type_profil =  forms.CharField(initial = 'Type de profil', choices=profil, widget=forms.RadioSelect(attrs={'class': 'form-control'}))

    type_profil = forms.MultipleChoiceField(initial = 'Profil', widget=forms.Select(attrs={'class': 'form-control'}),
                                              choices=profil)

    nb_batiment = forms.IntegerField(initial='Nombre de bâtiments de ce type',
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}))

    categ = [
        ('Petit', 'Petit (< 150m²)'),
        ('Moyen', 'Moyen (150-500m²)'),
        ('Grand', 'Grand (500m²-1000m²)'),
        ('Tres grand', 'Très grand (> 1000m²)'),
    ]
    ##taille = forms.CharField(initial ='Catégorie de taille', choices = categ,
                                    ##widget= forms.TextInput(attrs={'class': 'form-control-range', 'type': 'range'}))

    taille = forms.MultipleChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                        choices=categ)


    type = (('Tôle', 'Tôle'),
        ('Tôle bac acier trapézoïdal','Tôle bac acier trapézoïdal'),
    )

    ##toiture =  forms.CharField(initial = 'Type de toiture', choices=type, widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    toiture = forms.MultipleChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
                                       choices=type)

    instal = ( (1,'Monophasée'),
                (0,'Triphasée'),
          )
    installation = forms.ChoiceField(choices=instal,widget=forms.Select(attrs={'class': 'form-control'}))

    puissance = forms.IntegerField(initial='Puissance souscrite',
                                     widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '150'}))

    ref = ( ('Mensuelle','Mensuelle '),
            ('Bimestrielle','Bimestrielle '),
            ('Annuelle','Annuelle '))

    reference = forms.ChoiceField(initial= 'Reference', choices=ref,widget=forms.Select(attrs={'class': 'form-control'}))

    nb_kW = forms.IntegerField(initial='Nombre KWh facture',
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '3084'}))

    facture = forms.IntegerField(initial='Montant facture ',
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1800 €'}))











