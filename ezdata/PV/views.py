# coding=utf-8
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .solutions import solution_GT, calcul_taux_centraleGT
from .forms import ClientForm, EnseigneForm, ProfilForm, ElectrificationForm, LocalisationForm, BatimentForm, \
    SouscriptionForm, ToitureForm
import plotly
from django.db import transaction
from django.contrib import messages
from .forms import Client
from .dimens_centrale import courbe_de_charges
import numpy as np
import matplotlib
matplotlib.use('Agg')
import io, base64
import matplotlib.pyplot as plt




@transaction.non_atomic_requests
def base(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render(request=request))


@transaction.non_atomic_requests
def clients(request):
    global formA
    global formB
    global formC
    global formD
    global formE
    global formF
    global formG
    global formH
    if request.method == 'POST':
        form_client = ClientForm(data=request.POST)
        form_enseigne = EnseigneForm(data=request.POST)
        form_loca = LocalisationForm(data=request.POST)
        form_elec = ElectrificationForm(data=request.POST)
        form_profil = ProfilForm(data=request.POST)
        form_batiment = BatimentForm(data=request.POST)
        form_toiture = ToitureForm(data=request.POST)
        form_edf = SouscriptionForm(data=request.POST)

        form_client_valid = form_client.is_valid()
        form_enseigne_valid = form_enseigne.is_valid()
        form_loca_valid = form_loca.is_valid()
        form_elec_valid = form_elec.is_valid()
        form_profil_valid = form_profil.is_valid()
        form_batiment_valid = form_batiment.is_valid()
        form_toiture_valid = form_toiture.is_valid()
        form_EDF_valid = form_edf.is_valid()

        # Verification de la validité des données
        if (form_client_valid and form_batiment_valid and form_loca_valid and form_elec_valid and \
                form_profil_valid and form_toiture_valid and form_enseigne_valid and form_EDF_valid):



            instance = form_client.save()
            instance1=form_enseigne.save(commit=False)
            instance2= form_batiment.save(commit=False)
            instance3 = form_loca.save(commit=False)
            instance4 = form_elec.save(commit=False)
            instance5 = form_profil.save(commit=False)
            instance6 = form_toiture.save(commit=False)
            instance7 = form_edf.save(commit=False)

            instance1.client = instance
            instance2.enseigne= instance1
            instance3.batiment = instance2
            instance4.souscription = instance7
            instance5.batiment = instance2
            instance6.batiment = instance2
            instance7.batiment = instance2

            form_enseigne.save()
            form_batiment.save()
            form_loca.save()
            form_edf.save()
            form_elec.save()
            form_profil.save()
            form_toiture.save()

            territ = form_loca.cleaned_data['territ']
            profil = form_profil.cleaned_data['type_profil']
            surface = form_toiture.cleaned_data['surface']
            puissance = form_edf.cleaned_data['puissance']
            installation = form_elec.cleaned_data['installation']
            conso_perso = form_edf.cleaned_data['nb_kW']
            ref = form_edf.cleaned_data['reference']
            if ref == 'Bimescourbe_irradiationtrielle':
                conso_perso = ((conso_perso * 6) / 365) * 7
            if ref == 'Mensuelle':
                conso_perso = ((conso_perso * 12) / 365) * 7

            result = solution_GT(conso_perso, profil, territ, surface, installation, puissance)
            taille = result[0]
            nbr_modules = result[1]
            surface_totale= result[2]
            n_solution = result[3]
            #fig = plot_courbes(conso_perso, profil, territ, surface, installation, puissance)


                # Premier graphique : jour ouvré

            #fig = plt.figure(1, figsize=(15, 5))

            coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0] / 1000

            #hours = ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00",
            #        "11:00", "12:00",
            #        "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00",
            #        "23:00"]
            #plt.title("PROFIL ENERGETIQUE : JOUR OUVRE MOYEN")

            #plt.plot(hours, coeffs_ouvre, color='r', label="Courbe de charge")

            tab = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[0]
            result1 = tab[:, 1] / 1000

                # Surface pour l'energie PV consomé

            surface = np.zeros((24, 1), float)
            for i in range(24):
                surface[i] = min(result1[i], coeffs_ouvre[i])
            surface = surface.flatten()

            #plt.plot(hours, result1, color='g', label="Production PV centrale proposée")

            #plt.fill_between(hours, surface, color='#FFA500', label="Energie PV consommée")

            #plt.legend()

            # Deuxième graphique : weekend

            #fig = plt.figure(2, figsize=(15, 5))

            #coeffs_weekend = courbe_de_charges(conso_perso, profil)[1] / 1000
            #plt.title("PROFIL ENERGETIQUE : WEEKEND MOYEN")

            #plt.plot(hours, coeffs_weekend, color='r', label="Courbe de charge")
            #tab = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[0]
            #result1 = tab[:, 1] / 1000

            # Surface pour l'energie PV consomé

            #surface = np.zeros((24, 1), float)
            #for i in range(24):
             #   surface[i] = min(result1[i], coeffs_weekend[i])
            #surface = surface.flatten()

            #plt.plot(hours, result1, color='g', label="Production PV centrale proposée")

            #plt.fill_between(hours, surface, color='#FFA500', label="Energie PV consommée")

            #plt.legend()
            #flike = io.BytesIO()
            #fig.savefig(flike)
            #b64 = base64.b64encode(flike.getvalue()).decode()
            #context['chart'] = b64


            #graph_div = plotly.offline.plot(fig, auto_open=False, output_type="div")

            return render(request, 'chart.html', {'taille': taille,'nb_modules':nbr_modules, 'surface': surface_totale, 'n': n_solution, 'graph1': coeffs_ouvre,
                                                'surface1': surface})


        else :
            #messages.error(request, "Error")
            print (form_client.errors)
            print (form_batiment.errors)
            print (form_loca.errors)
            print (form_elec.errors)
            print (form_profil.errors)
            print (form_batiment.errors)
            print (form_toiture.errors)
            print (form_edf.errors)

    else:
        formA = ClientForm()
        formB = EnseigneForm()
        formC = LocalisationForm()
        formD = ElectrificationForm()
        formE = ProfilForm()
        formF = ToitureForm()
        formG = BatimentForm()
        formH = SouscriptionForm()

    return render(request, 'wizard-create-profile.html', {'formA': formA, 'formB': formB,
                                                          'formC': formC, 'formD':  formD,
                                                          'formE': formE , 'formF': formF,
                                                          'formG': formG , 'formH': formH})
