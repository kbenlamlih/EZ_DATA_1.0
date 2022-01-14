# coding=utf-8
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .solutions import solution_GT, calcul_taux_centraleGT,Economies_pv
from .forms import ClientForm, EnseigneForm, ProfilForm, ElectrificationForm, LocalisationForm, BatimentForm, \
    SouscriptionForm, ToitureForm, MobiliteForm
from django.db import transaction
from django.contrib import messages
from .forms import Client
from .dimens_centrale import courbe_de_charges
import numpy as np
from .facturation import calcu_prix, total_HA,total_Transport, total_Marge, total_prix
from .MDE import coeffs_mde, Economies, Invest
from .mobilite import Vehicule_thermique_annuel, Vehicule_electrique_annuel, Tableau_Bornes,Differenciel,Economies_mobilite
from .models import Emisission_CO2
from .Bilan import Bilan2



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
    global formI
    if request.method == 'POST':
        form_client = ClientForm(data=request.POST)
        form_enseigne = EnseigneForm(data=request.POST)
        form_loca = LocalisationForm(data=request.POST)
        form_elec = ElectrificationForm(data=request.POST)
        form_profil = ProfilForm(data=request.POST)
        form_batiment = BatimentForm(data=request.POST)
        form_toiture = ToitureForm(data=request.POST)
        form_edf = SouscriptionForm(data=request.POST)
        form_mobilite=MobiliteForm(data=request.POST)

        form_client_valid = form_client.is_valid()
        form_enseigne_valid = form_enseigne.is_valid()
        form_loca_valid = form_loca.is_valid()
        form_elec_valid = form_elec.is_valid()
        form_profil_valid = form_profil.is_valid()
        form_batiment_valid = form_batiment.is_valid()
        form_toiture_valid = form_toiture.is_valid()
        form_EDF_valid = form_edf.is_valid()
        form_mobilite_valid= form_mobilite.is_valid()

        # Verification de la validité des données
        if (form_client_valid and form_batiment_valid and form_loca_valid and form_elec_valid and \
                form_profil_valid and form_toiture_valid and form_enseigne_valid and form_EDF_valid and form_mobilite_valid):



            instance = form_client.save()
            instance1=form_enseigne.save(commit=False)
            instance2= form_batiment.save(commit=False)
            instance3 = form_loca.save(commit=False)
            instance4 = form_elec.save(commit=False)
            instance5 = form_profil.save(commit=False)
            instance6 = form_toiture.save(commit=False)
            instance7 = form_edf.save(commit=False)
            instance8=form_mobilite.save(commit=False)

            instance1.client = instance
            instance2.enseigne= instance1
            instance3.batiment = instance2
            instance4.souscription = instance7
            instance5.batiment = instance2
            instance6.batiment = instance2
            instance7.batiment = instance2
            instance8.batiment = instance2

            form_enseigne.save()
            form_batiment.save()
            form_loca.save()
            form_edf.save()
            form_elec.save()
            form_profil.save()
            form_toiture.save()
            form_mobilite.save()

            #Enregistrer toutes les infos du client pour les utiliser dans les autres vues
            request.session['nom_entreprise'] = form_client.cleaned_data['nom_entreprise']
            request.session['toiture'] = form_toiture.cleaned_data['toiture']
            request.session['facture']= form_edf.cleaned_data['facture']
            request.session['nb_etages']= form_batiment.cleaned_data['nb_etages']
            request.session['type_batiment']= form_batiment.cleaned_data['type_batiment']
            request.session['vehicule_fonction']= form_mobilite.cleaned_data['vehicule_fonction']
            request.session['km_an_vehicule_fonction']= form_mobilite.cleaned_data['km_an_vehicule_fonction']
            request.session['vehicule_utilitaire']= form_mobilite.cleaned_data['vehicule_utilitaire']
            request.session['km_an_vehicule_utilitaire']= form_mobilite.cleaned_data['km_an_vehicule_utilitaire']
            request.session['parking']= form_mobilite.cleaned_data['parking']
            request.session['acces']= form_mobilite.cleaned_data['acces']
            request.session['borne']= form_mobilite.cleaned_data['borne']
            request.session['pt_de_charge']= form_mobilite.cleaned_data['pt_de_charge']
            request.session['nb_batiment']= form_batiment.cleaned_data['nb_batiment']

            request.session['territ']= form_loca.cleaned_data['territ']
            territ = request.session['territ']

            request.session['type_profil'] =form_profil.cleaned_data['type_profil']
            profil =  request.session['type_profil']

            request.session['surface'] = form_toiture.cleaned_data['surface']
            surface = request.session['surface']

            request.session['puissance']= form_edf.cleaned_data['puissance']
            puissance = request.session['puissance']

            request.session['installation']= form_elec.cleaned_data['installation']
            installation = request.session['installation']

            request.session['nb_kW']=  form_edf.cleaned_data['nb_kW']
            conso_perso = request.session['nb_kW']

            request.session['reference']= form_edf.cleaned_data['reference']
            ref = request.session['reference']

            if ref == 'Bimestrielle':
                conso_perso = ((conso_perso * 6) / 365) * 7
            if ref == 'Mensuelle':
                conso_perso = ((conso_perso * 12) / 365) * 7

            result = solution_GT(conso_perso, profil, territ, surface, installation, puissance)
            taille = result[0]
            nbr_modules = result[1]
            surface_totale= result[2]
            n_solution = result[3]

            coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0] / 1000
            # Pour afficher les courbes dans le bon format

            out = np.array(coeffs_ouvre).flatten().tolist()
            tab = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[0]
            result1 = tab[:, 1] / 1000
            out1 = np.array(result1).flatten().tolist()

            surface_graph = np.zeros((24, 1), float)
            for i in range(24):
                surface_graph[i] = min(result1[i], coeffs_ouvre[i])
            surface_graph = surface_graph.flatten().tolist()

            coeffs_ouvre1 = courbe_de_charges(conso_perso, territ)[1] / 1000
            # Pour afficher les courbes dans le bon format

            out2 = np.array(coeffs_ouvre1).flatten().tolist()
            surface_graph1 = np.zeros((24, 1), float)
            for i in range(24):
                surface_graph1[i] = min(result1[i], coeffs_ouvre1[i])
            surface_graph1 = surface_graph1.flatten().tolist()

            auto_conso = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[1]
            auto_prod = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[2]

            return render(request, 'dashboard_2.html',
                          {'taille': taille, 'nb_modules': nbr_modules, 'surface': surface_totale, 'n': n_solution,
                           'graph1': out, 'graph2': out1, 'graph3': surface_graph, 'graph4': out2,
                           'graph5': surface_graph1, 'surface1': surface, 'autoconso': auto_conso,
                           'autoprod': auto_prod})

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
            print(form_mobilite.errors)

    else:
        formA = ClientForm()
        formB = EnseigneForm()
        formC = LocalisationForm()
        formD = ElectrificationForm()
        formE = ProfilForm()
        formF = ToitureForm()
        formG = BatimentForm()
        formH = SouscriptionForm()
        formI= MobiliteForm()

    return render(request, 'wizard-create-profile.html', {'formA': formA, 'formB': formB,
                                                          'formC': formC, 'formD':  formD,
                                                          'formE': formE , 'formF': formF,
                                                          'formG': formG , 'formH': formH, 'formI':formI})

def results(request):

    territ = request.session['territ']

    profil = request.session['type_profil']

    surface = request.session['surface']

    puissance = request.session['puissance']

    installation = request.session['installation']

    conso_perso = request.session['nb_kW']

    ref = request.session['reference']

    if ref == 'Bimestrielle':
        conso_perso = ((conso_perso * 6) / 365) * 7
    if ref == 'Mensuelle':
        conso_perso = ((conso_perso * 12) / 365) * 7

    result = solution_GT(conso_perso, profil, territ, surface, installation, puissance)
    taille = result[0]
    nbr_modules = result[1]
    surface_totale = result[2]
    n_solution = result[3]

    coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0] / 1000
    # Pour afficher les courbes dans le bon format

    out = np.array(coeffs_ouvre).flatten().tolist()
    tab = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[0]
    result1 = tab[:, 1] / 1000
    out1 = np.array(result1).flatten().tolist()

    surface_graph = np.zeros((24, 1), float)
    for i in range(24):
        surface_graph[i] = min(result1[i], coeffs_ouvre[i])
    surface_graph = surface_graph.flatten().tolist()

    coeffs_ouvre1 = courbe_de_charges(conso_perso, territ)[1] / 1000
    # Pour afficher les courbes dans le bon format

    out2 = np.array(coeffs_ouvre1).flatten().tolist()
    surface_graph1 = np.zeros((24, 1), float)
    for i in range(24):
        surface_graph1[i] = min(result1[i], coeffs_ouvre1[i])
    surface_graph1 = surface_graph1.flatten().tolist()

    auto_conso = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[1]
    auto_conso=round(auto_conso,2)
    auto_prod = calcul_taux_centraleGT(conso_perso, profil, territ, surface, installation, puissance)[2]
    auto_prod=round(auto_prod,2)

    return render(request, 'dashboard_2.html',
                  {'taille': taille, 'nb_modules': nbr_modules, 'surface': surface_totale, 'n': n_solution,
                   'graph1': out, 'graph2': out1, 'graph3': surface_graph, 'graph4': out2,
                   'graph5': surface_graph1, 'surface1': surface, 'autoconso': auto_conso,
                   'autoprod': auto_prod})

def factu(request):

    territ = request.session['territ']
    profil = request.session['type_profil']
    surface = request.session['surface']
    puissance = request.session['puissance']
    installation = request.session['installation']
    conso_perso = request.session['nb_kW']
    toiture = request.session['toiture']


    result = solution_GT(conso_perso, profil, territ, surface, installation, puissance)
    taille = result[0]
    nbr_modules = result[1]
    surface_totale = result[2]
    n_solution = result[3]

    test =calcu_prix(taille, toiture, territ, installation,n_solution)
    p1= total_HA(taille, toiture, territ, installation,n_solution)

    p2=total_Transport(taille, toiture, territ, installation,n_solution)
    p3=total_Marge(taille, toiture, territ, installation,n_solution)
    p4=total_prix(taille, toiture, territ, installation,n_solution)



    return render (request, 'factu.html', {'module': test, 'totalHA':p1, 'totalTransport':p2, 'totalMarge':p3, 'totalPrix':p4})


def mde(request):
    territ = request.session['territ']
    NbrekWhfacture = request.session['nb_kW']
    Recurrencefacture=request.session['reference']
    Montantfacture=request.session['facture']
    Surfacetoiture=request.session['surface']
    Nbreetages=  request.session['nb_etages']
    type=request.session['type_batiment']


    ancienne_conso= coeffs_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages,type )[0]
    conso_reduite= coeffs_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages,type )[1]

    difference= coeffs_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages,type )[3]

    Bilan_Economique=Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ)[0]
    Bilan_Energetique=Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ)[1]
    Bilan_Environnemental= Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ)[2]

    invest= Invest(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ)

    #Calculs pour Emission C02 des Bâtiments
    rqt0=Emisission_CO2.objects.get(territ=territ)
    emission_coeff= rqt0.emission

    emission_avant_1an= NbrekWhfacture*emission_coeff
    emission_avant_10ans=emission_avant_1an*10
    emission_avant_20ans=emission_avant_10ans*2
    emission_avant=[emission_avant_1an,emission_avant_10ans,emission_avant_20ans ]

    emission_apres_1an= emission_avant_1an-Bilan_Environnemental[0]
    emission_apres_10ans = emission_avant_10ans-Bilan_Environnemental[1]
    emission_apres_20ans = emission_avant_20ans -Bilan_Environnemental[2]
    emission_apres = [emission_apres_1an, emission_apres_10ans, emission_apres_20ans]


    return render(request, 'mde.html',{'courbe1': ancienne_conso, 'courbe2':conso_reduite, 'area':difference,
                                       'bilan1':Bilan_Economique, 'bilan2': Bilan_Energetique, 'bilan3': Bilan_Environnemental, 'Investissement': invest,
                                       'emissions_avant': emission_avant, 'emission_apres':emission_apres})

def mobi(request):
    territ = request.session['territ']
    NbreVS= request.session['vehicule_fonction']
    NbkmanVS= request.session['km_an_vehicule_fonction']
    NbreVU= request.session['vehicule_utilitaire']
    NbkmanVU= request.session['km_an_vehicule_utilitaire']
    Presenceparking= request.session['parking']
    Nb_pdc_choisi=request.session['pt_de_charge']
    Accessibilite_parking=request.session['acces']
    Optionborne=request.session['borne']

#1er graph : Economies en changant de voiture : passage du thermique a l'eletrique
    courbe1= Vehicule_thermique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU)[4]
    courbe1 = courbe1.flatten().tolist()

    courbe2= Vehicule_electrique_annuel(NbreVS, NbkmanVS, NbreVU, NbkmanVU)[3]

    courbe2_abo= Tableau_Bornes(Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne, NbreVS, NbreVU)[2]

    courbe2_coeffs= courbe2 + courbe2_abo
    courbe2_coeffs = courbe2_coeffs.flatten().tolist()


    courbe4= Differenciel(NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi, Accessibilite_parking,
                     Optionborne)
    Bilan_Economique_mobilite= Economies_mobilite(territ,NbreVS,NbkmanVS,NbreVU,NbkmanVU,Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne)[0]
    Bilan_Environnemental_mobilite=Economies_mobilite(territ,NbreVS,NbkmanVS,NbreVU,NbkmanVU,Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne)[1]

    return render(request, 'mobilite.html',{'courbe1': courbe1, 'courbe2':courbe2_coeffs,
                                       'bilan1':Bilan_Economique_mobilite, 'bilan3': Bilan_Environnemental_mobilite})

def bilan(request):
    #conso_perso = request.session['nb_kW']

    #ref = request.session['reference']

    #if ref == 'Bimestrielle':
    #    conso_perso = ((conso_perso * 6) / 365) * 7
    #if ref == 'Mensuelle':
    #    conso_perso = ((conso_perso * 12) / 365) * 7

    #profil= request.session['profil']
    #profil = 'Tertiaire'
    #surface= request.session['surface']
    #installation= request.session['installation']
   # puissance= request.session['puissance']
    #territ = request.session['territ']



    #NbrekWhfacture = request.session['nb_kW']
   # Recurrencefacture = request.session['reference']
    #Montantfacture = request.session['facture']
   # Nbreetages = request.session['nb_etages']
   # type = request.session['type_batiment']
   # nb_batiment= request.session['nb_batiment']
    #NbreVS = request.session['vehicule_fonction']
    #NbkmanVS = request.session['km_an_vehicule_fonction']
    #NbreVU = request.session['vehicule_utilitaire']
    #NbkmanVU = request.session['km_an_vehicule_utilitaire']
    #Presenceparking = request.session['parking']
    #Nb_pdc_choisi = request.session['pt_de_charge']
    #Accessibilite_parking = request.session['acces']
    #Optionborne = request.session['borne']

    NbreVS = 2
    NbkmanVS = 20000
    NbreVU = 2
    NbkmanVU = 23000
    Presenceparking = 'Non'
    Nb_pdc_choisi = 2
    Accessibilite_parking = 'Public'
    Optionborne = 'Non'
    conso_perso = 115.07
    profil = 'Tertiaire'
    territ = 'Guadeloupe'
    surface = 200
    installation = 'Triphasée'
    puissance = 150
    NbrekWhfacture = 6000
    Recurrencefacture = 'Annuelle'
    Montantfacture = 2700
    Nbreetages = 2
    type = 'BTP'
    nb_batiment=4

    rqt0= Emisission_CO2.objects.get(territ=territ)
    Emission_CO2=rqt0.emission

    Economies_mde=  Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages, type, territ)
    Economies_PV= Economies_pv(conso_perso, profil, territ, surface,installation, puissance,NbrekWhfacture,Recurrencefacture,Montantfacture,Nbreetages,type)
    Economies_Mobilite= Economies_mobilite(territ, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking, Nb_pdc_choisi,Accessibilite_parking, Optionborne, NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages)

    Bilan_apres= Bilan2(conso_perso, profil, territ, surface, installation, puissance, NbrekWhfacture, Recurrencefacture,
           Montantfacture, Nbreetages, type, NbreVS, NbkmanVS, NbreVU, NbkmanVU, Presenceparking,
           Nb_pdc_choisi, Accessibilite_parking, Optionborne,nb_batiment)

    Economique_mde=round(Economies_mde[0][2]/20*nb_batiment,2)
    Economique_pv= round(Economies_PV[0][2]/20*nb_batiment,2)
    Economique_mobilite= round((Economies_Mobilite[0][2]/20),2)
    Total_Economique= round(Economique_mde+Economique_pv+Economique_mobilite,2)

    Environnement_mde=round(Economies_mde[2][2]/20*nb_batiment,2)
    Environnement_pv=round(Economies_PV[2][2]/20*nb_batiment,2)
    Environnement_mobilite= round(Economies_Mobilite[1][2]/20,2)
    Total_Environnement= round(Environnement_mde+Environnement_pv+Environnement_mobilite,2)

    Energie_mde=round(Environnement_mde/Emission_CO2/1000,2)
    Energie_pv= round(Environnement_pv/Emission_CO2/1000,2)
    Total_Energie= round(Energie_mde+Environnement_pv+Energie_pv,2)


    Investissement_mde = Invest(NbrekWhfacture, Recurrencefacture, Montantfacture, surface, Nbreetages, type, territ)
    Investissement_mde= Investissement_mde/20

    coeff_un=round(Economies_mde[2][2]*nb_batiment,1)
    coeff_deux=round(Economies_PV[2][2]*nb_batiment,1)
    coeff_trois= round(Economies_Mobilite[1][2],1)
    total= Bilan_apres[2][8]-(coeff_un+coeff_deux+coeff_trois)
    coeff_quatre= Bilan_apres[2][6]
    print(Bilan_apres)

    return render(request,'bilan.html',{'un': Economique_mde, 'deux':Economique_pv, 'trois':Economique_mobilite, 'quatre':Total_Economique,
                                        'cinq':Environnement_mde, 'six':Environnement_pv, 'sept':Environnement_mobilite, 'huit':Total_Environnement,
                                        'neuf':Energie_mde, 'dix':Energie_pv, 'onze':Total_Energie,
                                        'Emission_bâtiment': coeff_un, 'Emisssion':coeff_deux})



