from django.contrib import admin
from django.shortcuts import render, redirect
from .models import ModulesPV
from .models import BDD
from .models import Client
from .forms import CsvImportForm
from .utils import ExportCsvMixin
from django.urls import path
import csv
from io import TextIOWrapper
from import_export.admin import ImportExportModelAdmin




admin.site.register(ModulesPV)
#admin.site.register(BDD)

#@admin.register(BDD)

class BDDAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display=["N","Onduleur_1","Batterie_1", "Nombre_Batterie_1", "Onduleur_2","Batterie_2","Nombre_Batterie_2","Onduleur_3",
                  "Module_batterie_1", "Module_batterie_2", "Electrical_installation","Nb_modules_min","Puissance_centrale_max", "Capacit_batterie",
                   "Prix_total_achat"]

admin.site.register(BDD, BDDAdmin)

admin.site.register(Client)
