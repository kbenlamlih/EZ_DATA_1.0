import numpy as np
from .models import Emisission_CO2,Hyp_cout_mobilite,EZ_DRIVE


### Variables statiques ###
rqt0=Hyp_cout_mobilite.objects.get(model="Prix véhicule + maintenance Electrique")  # €/mois
Prix_vehicule_electrique = rqt0.valeur

rqt1=Hyp_cout_mobilite.objects.get(model="Prix véhicule + maintenance Thermique")  # €/mois
Prix_vehicule_thermique = rqt1.valeur

rqt2=Hyp_cout_mobilite.objects.get(model="Prix véhicule utililaire + maintenance Electrique")  # €/mois
Prix_utililaire_electrique = rqt2.valeur

rqt3= Hyp_cout_mobilite.objects.get(model="Prix véhicule utilitaire + maintenance Thermique")  #€/mois
Prix_utililaire_thermique = rqt3.valeur

rqt4= Hyp_cout_mobilite.objects.get(model="Prix électricité")  #€/mois
Prix_electricite = rqt4.valeur

rqt5 = Hyp_cout_mobilite.objects.get(model="Prix carburant initial")  #€/mois
Prix_carburant_initial = rqt5.valeur

rqt6 = Hyp_cout_mobilite.objects.get(model="Augmentation prix électricité")  #€/mois
Augmentation_prix_electricite = rqt6.valeur

rqt7= Hyp_cout_mobilite.objects.get(model="Augmentation prix carburant")  # €/mois
Augmentation_prix_carburant = rqt7.valeur

rqt8= Hyp_cout_mobilite.objects.get(model="Consommation véhicule Electrique")  #  kWh/100km
Consommation_vehicule_electrique = rqt8.valeur

rqt9= Hyp_cout_mobilite.objects.get(model="Consommation véhicule Thermique") # L/100km
Consommation_vehicule_thermique = rqt9.valeur

rqt10= Hyp_cout_mobilite.objects.get(model="Consommation utilitaire Electrique")# kWh/100km
Consommation_utilitaire_electrique = rqt10.valeur

rqt11= Hyp_cout_mobilite.objects.get(model="Consommation utilitaire Thermique")#  L/100km
Consommation_utilitaire_thermique = rqt11.valeur


rqt12= EZ_DRIVE.objects.get(model="Prix borne simple PRIVATE") # €/mois
Prix_borne_simple_PRIVATE = rqt12.valeur

rqt13= EZ_DRIVE.objects.get(model="Prix borne double PRIVATE") # €/mois
Prix_borne_double_PRIVATE = rqt13.valeur

rqt14= EZ_DRIVE.objects.get(model="Prix borne simple PUBLIC") # €/mois
Prix_borne_simple_PUBLIC = rqt14.valeur

rqt15= EZ_DRIVE.objects.get(model="Prix borne double PUBLIC") # €/mois
Prix_borne_double_PUBLIC = rqt15.valeur

Investissement_initial_borne_simple_PRIVATE = rqt12.invest  # €
Investissement_initial_borne_simple_PUBLIC = rqt14.invest  # €
Investissement_initial_borne_double_PRIVATE = rqt13.invest  # €
Investissement_initial_borne_double_PUBLIC = rqt15.invest  # €

rqt16= EZ_DRIVE.objects.get(model="Bénéfice revente électricité borne PUBLIC")  # €/KWh

rqt17= EZ_DRIVE.objects.get(model="Estimation conso extérieur borne PUBLIC") # €/mois
Estim_conso_borne = rqt17.valeur

rqt18= EZ_DRIVE.objects.get(model="Abonnement EZ-Drive 150km") # €/mois
Abonnement_EZ_Drive_150km = rqt18.valeur

rqt19= EZ_DRIVE.objects.get(model="Abonnement EZ-Drive 300km") # €/mois
Abonnement_EZ_Drive_300km = rqt19.valeur

rqt20= EZ_DRIVE.objects.get(model="Abonnement EZ-Drive 600km") # €/mois
Abonnement_EZ_Drive_600km = rqt20.valeur

rqt21= Emisission_CO2.objects.get(territ="Litre d'essence")
prix_L_essence= rqt21.emission

### Données d'entrée à récupérer ###

NbreVS = 3  # Donnée à prendre dans les inputs clients#VS:vehicule salarie
NbreVU = 1  # Donnée à prendre dans les inputs clients#VS:vehicule utilitaire
NbkmanVS = 10000  # Donnée à prendre dans les inputs clients
NbkmanVU = 12000  # Donnée à prendre dans les inputs clients
Presenceparking = True  # Donnée à prendre dans les inputs clients
Accessibilite_parking = "Public"  # Donnée à prendre dans les inputs clients
Optionborne = True  # Donnée à prendre dans les inputs clients
Nb_pdc_choisi = 2  # Donnée à prendre dans les inputs clients

## Calcul tableau cout vehicule thermique année par année sur 20 ans ##
def Vehicule_thermique_annuel(NbreVS,NbkmanVS,NbreVU,NbkmanVU):
    Cout_vehicule_thermique_annuel = np.ones((5, 20))
    # [0,0]= cout vehicule l'année 1
    # [1,0]= prix carburant au litre l'année 1
    # [2,0]= cout total carburant sur l'année 1
    # [3,0]= litres carburant sur l'année 1
    # [4,0]= cout total sur l'année 1
    Cout_vehicule_thermique_annuel[0, 0] = 12 * (Prix_vehicule_thermique * NbreVS + Prix_utililaire_thermique * NbreVU)
    Cout_vehicule_thermique_annuel[1, 0] = Prix_carburant_initial
    Cout_vehicule_thermique_annuel[2, 0] = (NbreVS * NbkmanVS * Consommation_vehicule_thermique + NbreVU * NbkmanVU * Consommation_utilitaire_thermique) / 100 * \
                                           Cout_vehicule_thermique_annuel[1, 0]
    Cout_vehicule_thermique_annuel[3, 0] = Cout_vehicule_thermique_annuel[2, 0] / Cout_vehicule_thermique_annuel[1, 0]
    Cout_vehicule_thermique_annuel[4, 0] = Cout_vehicule_thermique_annuel[0, 0] + Cout_vehicule_thermique_annuel[2, 0]

    for i in range(1, 20):
        Cout_vehicule_thermique_annuel[0, i] = 12 * (Prix_vehicule_thermique * NbreVS + Prix_utililaire_thermique * NbreVU)
        Cout_vehicule_thermique_annuel[1, i] = Cout_vehicule_thermique_annuel[1, i - 1] * (
                    1 + Augmentation_prix_carburant / 100)
        Cout_vehicule_thermique_annuel[2, i] = (NbreVS * NbkmanVS * Consommation_vehicule_thermique + NbreVU * NbkmanVU * Consommation_utilitaire_thermique) / 100 * \
                                               Cout_vehicule_thermique_annuel[1, i]
        Cout_vehicule_thermique_annuel[3, i] = Cout_vehicule_thermique_annuel[2, i] / Cout_vehicule_thermique_annuel[1, i]
        Cout_vehicule_thermique_annuel[4, i] = Cout_vehicule_thermique_annuel[0, i] + Cout_vehicule_thermique_annuel[2, i]
    return Cout_vehicule_thermique_annuel

### Calcul tableau cout vehicule electrique année par année sur 20 ans ###
def Vehicule_electrique_annuel(NbreVS,NbkmanVS,NbreVU,NbkmanVU):
    Cout_vehicule_electrique_annuel = np.ones((4, 20))
    # [0,0]= cout vehicule l'année 1
    # [1,0]= prix kWh d'electricité l'année 1
    # [2,0]= cout total électricité sur l'année 1
    # [3,0]= cout total sur l'année 1
    Cout_vehicule_electrique_annuel[0, 0] = 12 * (Prix_vehicule_electrique * NbreVS + Prix_utililaire_electrique * NbreVU)
    Cout_vehicule_electrique_annuel[1, 0] = Prix_electricite
    Cout_vehicule_electrique_annuel[2, 0] = (NbreVS * NbkmanVS * Consommation_vehicule_electrique + NbreVU * NbkmanVU * Consommation_utilitaire_electrique) / 100 * \
                                            Cout_vehicule_electrique_annuel[1, 0]
    Cout_vehicule_electrique_annuel[3, 0] = Cout_vehicule_electrique_annuel[0, 0] + Cout_vehicule_electrique_annuel[2, 0]

    for i in range(1, 20):
        Cout_vehicule_electrique_annuel[0, i] = 12 * (
                    Prix_vehicule_electrique * NbreVS + Prix_utililaire_electrique * NbreVU)
        Cout_vehicule_electrique_annuel[1, i] = Cout_vehicule_electrique_annuel[1, i - 1] * (
                    1 + Augmentation_prix_electricite / 100)
        Cout_vehicule_electrique_annuel[2, i] = (
                                                            NbreVS * NbkmanVS * Consommation_vehicule_electrique + NbreVU * NbkmanVU * Consommation_utilitaire_electrique) / 100 * \
                                                Cout_vehicule_electrique_annuel[1, i]
        Cout_vehicule_electrique_annuel[3, i] = Cout_vehicule_electrique_annuel[0, i] + Cout_vehicule_electrique_annuel[2, i]
    return Cout_vehicule_electrique_annuel

### Calcul tableau investissment bornes ###

def Tableau_Bornes(Presenceparking,Nb_pdc_choisi,Accessibilite_parking,Optionborne, NbreVS,NbreVU):
    Investissement_bornes = np.zeros(4)
    # [0] = Investissement tous les 5 ans
    # [1] = Prix mensuel
    # [2] = Cout total sur 5 ans
    # [3] = Gains bornes publiques par an
    Nb_borne_double = 0
    Nb_borne_simple = 0

    if Presenceparking == 'Oui':
        if Optionborne == 'Oui':
            Nb_borne_double = Nb_pdc_choisi // 2
            Nb_borne_simple = Nb_pdc_choisi % 2

    if Optionborne=='Oui':
        if Accessibilite_parking == "Public":
            Investissement_bornes[
                0] = Nb_borne_double * Investissement_initial_borne_double_PUBLIC + Nb_borne_simple * Investissement_initial_borne_simple_PUBLIC
            Investissement_bornes[
                1] = Nb_borne_double * Prix_borne_double_PUBLIC + Nb_borne_simple * Prix_borne_simple_PUBLIC
        else:
            Investissement_bornes[
                0] = Nb_borne_double * Investissement_initial_borne_double_PRIVATE + Nb_borne_simple * Investissement_initial_borne_simple_PRIVATE
            Investissement_bornes[
                1] = Nb_borne_double * Prix_borne_double_PRIVATE + Nb_borne_simple * Prix_borne_simple_PRIVATE

    Investissement_bornes[2] = Investissement_bornes[0] + Investissement_bornes[1] * 12 * 5

    if Optionborne =='Oui' and Accessibilite_parking == "Public":
        Investissement_bornes[3] = Benefice_revente_elec * Estim_conso_borne * 365 * Nb_pdc_choisi

    ### Calcul des abonnements EZdrive si pas d'option borne ###

    Abonnement_EZ_Drive_salarie = 0
    Abonnement_EZ_Drive_utilitaire = 0

    if Optionborne =='Non':
        if (NbkmanVS / 12) < 150:
            Abonnement_EZ_Drive_salarie = NbreVS * Abonnement_EZ_Drive_150km
        if (NbkmanVS / 12) < 300:
            Abonnement_EZ_Drive_salarie = NbreVS * Abonnement_EZ_Drive_300km
        if (NbkmanVS / 12) >= 300:
            Abonnement_EZ_Drive_salarie = NbreVS * Abonnement_EZ_Drive_600km

        if (NbkmanVU / 12) < 150:
            Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_150km
        if (NbkmanVU / 12) < 300:
            Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_300km
        if (NbkmanVU / 12) >= 300:
            Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_600km

    ### Calcul du tableau bornes année par année sur 20 ans ###

    Bornes = np.zeros((3, 20))
    # [0,i]= Cout des bornes sur l'année i
    # [1,i]= Gains des bornes l'année i
    # [2,i]= Cout abonnements ezdrive l'année i
    for i in range(20):
        Bornes[0, i] = Investissement_bornes[1] * 12
        if i % 5 == 0:
            Bornes[0, i] += Investissement_bornes[0]
        Bornes[1, i] = Investissement_bornes[3]
        Bornes[2, i] = (Abonnement_EZ_Drive_salarie + Abonnement_EZ_Drive_utilitaire) * 12
    return Bornes

### Calcul du différentiel de cout entre vehicule thermique et electrique année par année sur 20 ans ###
def Differenciel(NbreVS,NbkmanVS,NbreVU,NbkmanVU,Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne):

    Differenciel_bornes = np.zeros((3, 20))  # Thermique - electrique
    Cout_vehicule_thermique_annuel= Vehicule_thermique_annuel(NbreVS,NbkmanVS,NbreVU,NbkmanVU)
    Cout_vehicule_electrique_annuel= Vehicule_electrique_annuel(NbreVS,NbkmanVS,NbreVU,NbkmanVU)
    Bornes= Tableau_Bornes(Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne, NbreVS, NbreVU)
    # [0,i]=Delta vehicules
    # [1,i]=Delta carburant
    # [2,i]=Delta total
    for i in range(20):
        Differenciel_bornes[0, i] = Cout_vehicule_thermique_annuel[0, i] - Cout_vehicule_electrique_annuel[0, i]
        Differenciel_bornes[1, i] = Cout_vehicule_thermique_annuel[2, i] - Cout_vehicule_electrique_annuel[2, i]
        Differenciel_bornes[2, i] = Cout_vehicule_thermique_annuel[4, i] - Cout_vehicule_electrique_annuel[3, i] - Bornes[
            0, i] + Bornes[1, i] - Bornes[2, i]
    return Differenciel_bornes

    ### Bilan des economies réalisables sur la mobilité ###

def Economies_mobilite(territ,NbreVS,NbkmanVS,NbreVU,NbkmanVU,Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne):
    rqt99= Emisission_CO2.objects.get(territ=territ)
    Emission_CO2= rqt99.emission
    Differenciel_bornes= Differenciel(NbreVS,NbkmanVS,NbreVU,NbkmanVU,Presenceparking, Nb_pdc_choisi, Accessibilite_parking, Optionborne)

    Bilan_mobilité = np.zeros((2, 3))
    # [0,0]=Economique sur 1 an en euros
    # [0,1]=Economique sur 10 ans
    # [0,2]=Economique sur 20 ans
    # [1,0]=Environnemental sur 1 an en kg de CO2
    # [1,1]=Environnemental sur 10 ans
    # [1,2]=Environnemental sur 20 ans
    Bilan_mobilité[0, 0] = Differenciel_bornes[2, 0]
    Bilan_mobilité[0, 1] = sum(Differenciel_bornes[2, :10])
    Bilan_mobilité[0, 2] = sum(Differenciel_bornes[2,])

    Bilan_mobilité[1, 0] = (NbkmanVS * NbreVS * Consommation_vehicule_thermique + NbreVU * NbkmanVU * Consommation_utilitaire_thermique) / 100 * \
                           prix_L_essence - ((NbkmanVS * NbreVS * Consommation_vehicule_electrique + NbreVU * NbkmanVU * Consommation_utilitaire_electrique) / 100 *
                                              Emission_CO2)
    Bilan_mobilité[1, 1] = Bilan_mobilité[1, 0] * 10
    Bilan_mobilité[1, 2] = Bilan_mobilité[1, 0] * 20

    Bilan_economique= Bilan_mobilité[0, :]
    Bilan_enviro=Bilan_mobilité[1, :]

    return Bilan_economique, Bilan_enviro