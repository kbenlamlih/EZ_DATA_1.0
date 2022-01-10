from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from .models import (Client,Enseigne,Batiment,EDF,Electrification,Toiture,Localisation,Profil,Mobilite,)


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['nom_entreprise', 'mail']


    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['nom_entreprise'].widget.attrs['placeholder'] = 'Green Technologie'
        self.fields['mail'].widget.attrs['placeholder'] = 'kenza.benlamlih@greentechnologie.net'


class LocalisationForm(ModelForm):
    class Meta:
        model = Localisation
        fields = ('territ',)
        widget = {'Territoire': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Martinique'}),
                  }
    def __init__(self, *args, **kwargs):
        super(LocalisationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['territ'].widget.attrs['placeholder'] = 'Martinique'

class EnseigneForm(ModelForm):
    class Meta:
        model = Enseigne
        fields = ('secteur', 'nb_sites', 'effectif')
        widget= { 'Secteur': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Services'}),
                 'Nombre de sites':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30'}),
                  'Effectif': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '150'}),
                 }
    def __init__(self, *args, **kwargs):
        super(EnseigneForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['secteur'].widget.attrs['placeholder'] = 'Services'
        self.fields['nb_sites'].widget.attrs['placeholder'] = '30'
        self.fields['effectif'].widget.attrs['placeholder'] = '150'

class BatimentForm(ModelForm):
    class Meta:
        model = Batiment
        fields = ('type_batiment', 'nb_batiment', 'taille','nb_etages',)
        widget = {'type_batiment': forms.Select(attrs={'class': 'form-control'}),
                  'nb_batiment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}),
                  'taille': forms.Select(attrs={'class': 'form-control'}),
                  'nb_etages': forms.Select(attrs={'class': 'form-control'})
                  }

    def __init__(self, *args, **kwargs):
        super(BatimentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['nb_batiment'].widget.attrs['placeholder'] = '10'
        self.fields['nb_etages'].widget.attrs['placeholder'] = '1'

class ProfilForm(ModelForm):
    class Meta :
        model = Profil
        fields = ('type_profil', )
        widget= { 'Profil' : forms.Select(attrs={'class': 'form-control'}),
                  }

    def __init__(self, *args, **kwargs):
        super(ProfilForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ToitureForm(ModelForm):
    class Meta:
        model = Toiture
        fields = ('toiture','surface')
        widget = {'Toiture': forms.Select(attrs={'class': 'form-control'}),
                  'Surface': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '150'}),
        }

    def __init__(self, *args, **kwargs):
        super(ToitureForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ElectrificationForm(ModelForm):
    class Meta:
        model = Electrification
        fields = ('installation',)
        widget = {'Installation ': forms.Select(attrs={'class': 'form-control'}),
                  }

    def __init__(self, *args, **kwargs):
        super(ElectrificationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class SouscriptionForm(ModelForm):
    class Meta:
        model = EDF
        fields = ('puissance', 'reference', 'nb_kW', 'facture')
        widget = {'Puissance Souscrite ': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '150'}),
                  'Reference': forms.Select(attrs={'class': 'form-control'}),
                  'Nombre KWh facture':forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '3084'}),
                  'Montant facture': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1800€'}),
                  }
    def __init__(self, *args, **kwargs):
        super(SouscriptionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['puissance'].widget.attrs['placeholder'] = '150'
        self.fields['nb_kW'].widget.attrs['placeholder'] = '3084'
        self.fields['facture'].widget.attrs['placeholder'] = '1800€'


class MobiliteForm(ModelForm):
    class Meta :
        model = Mobilite
        fields= ('vehicule_fonction','km_an_vehicule_fonction','vehicule_utilitaire','km_an_vehicule_utilitaire','parking',
                 'acces','borne', 'pt_de_charge')

    def __init__(self, *args, **kwargs):
        super(MobiliteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['vehicule_fonction'].widget.attrs['placeholder'] = '2'
        self.fields['km_an_vehicule_fonction'].widget.attrs['placeholder'] = '10.000 km/an'
        self.fields['vehicule_utilitaire'].widget.attrs['placeholder'] = '2'
        self.fields['km_an_vehicule_utilitaire'].widget.attrs['placeholder'] = '23.000 km/an'
        self.fields['pt_de_charge'].widget.attrs['placeholder'] = '4'

