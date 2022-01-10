from django.contrib import admin
from django.shortcuts import render, redirect
from .models import (ModulesPV,BDD, Modules_factu, Taxe,Onduleurs, Monitoring, Main_doeuvre, Tableaux, Cables, Cheminement, Divers, Inge,Structure,BDDBat ,
                     EZ_DRIVE,Hyp_cout_mobilite, Emisission_CO2 )
from .forms import CsvImportForm
from .utils import ExportCsvMixin
from django.urls import path
import csv
from io import TextIOWrapper
from import_export.admin import ImportExportModelAdmin




admin.site.register(ModulesPV)
admin.site.register(Taxe)
admin.site.register(Modules_factu)


#admin.site.register(BDD)

#@admin.register(BDD)

class BDDAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=["N","Onduleur_1","Batterie_1", "Nombre_Batterie_1", "Onduleur_2","Batterie_2","Nombre_Batterie_2","Onduleur_3",
                  "Module_batterie_1", "Module_batterie_2", "Electrical_installation","Nb_modules_min","Puissance_centrale_max", "Capacit_batterie",
                   "Prix_total_achat"]

admin.site.register(BDD, BDDAdmin)

class OnduleursAdmin(ImportExportModelAdmin, admin.ModelAdmin) :
    list_display = ["model", "nom_francais", "nom_anglais","cout",	"install","tension", "puissance_dc", "puissance_ac"]

admin.site.register(Onduleurs, OnduleursAdmin)

class MonitoringAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout", "puissance_max"]

class Main_doeuvreAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout"]

class TableauxAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout"]

class CablesAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout"]

class CheminementAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout"]

class DiversAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout"]

class IngeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout"]

class StructureAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "nom_francais", "nom_anglais","cout"]

class BDDBatAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["type", "moy_kWh_avant", "moy_kWh_apres","moy_euros_avant","moy_euros_apres","cout_kWh_avant","cout_kWh_apres","gain"]

class Emisission_CO2Admin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["territ", "emission"]

class Hyp_cout_mobiliteAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "valeur", "unite"]

class EZ_DRIVEAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["model", "valeur", "unite","invest"]

admin.site.register(Monitoring, MonitoringAdmin)
admin.site.register(Main_doeuvre, Main_doeuvreAdmin)
admin.site.register(Tableaux, TableauxAdmin)
admin.site.register(Cables, CablesAdmin)
admin.site.register(Cheminement, CheminementAdmin)
admin.site.register(Divers, DiversAdmin)
admin.site.register(Inge, IngeAdmin)
admin.site.register(Structure, StructureAdmin)
admin.site.register(BDDBat, BDDBatAdmin)
admin.site.register(Emisission_CO2, Emisission_CO2Admin)
admin.site.register(Hyp_cout_mobilite, Hyp_cout_mobiliteAdmin)
admin.site.register(EZ_DRIVE, EZ_DRIVEAdmin)














