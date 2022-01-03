# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 10:06:20 2021

@author: Vianney Colliot
"""
import numpy as np

# Variables statiques
Prix_vehicule_electrique= 500 # €/mois
Prix_vehicule_thermique= 450 # €/mois
Prix_utililaire_electrique= 600 # €/mois
Prix_utililaire_thermique = 550 # €/mois
Prix_electricite = 0.15 # €/mois
Prix_carburant_initial =1.5 # €/mois
Augmentation_prix_electricite = 0.025 # %/ an
Augmentation_prix_carburant = 0.015 # %/ an
Consommation_vehicule_electrique= 15 # kWh/100km
Consommation_vehicule_thermique= 7.5 # L/100km
Consommation_utilitaire_electrique= 19  # kWh/100km
Consommation_utilitaire_thermique= 10 # L/100km

Prix_borne_simple_PRIVATE = 50 # €/mois
Prix_borne_double_PRIVATE = 100 # €/mois
Prix_borne_simple_PUBLIC = 60 # €/mois
Prix_borne_double_PUBLIC = 75 # €/mois
Investissement_initial_borne_simple_PRIVATE = 200 # €
Investissement_initial_borne_simple_PUBLIC = 200 # €
Investissement_initial_borne_double_PRIVATE = 300 # €
Investissement_initial_borne_double_PUBLIC = 300 # €

Benefice_revente_elec= 0.05 # €/KWh
Estim_conso_borne = 40  # kWh/jour
Abonnement_EZ_Drive_150km = 9 # €/mois
Abonnement_EZ_Drive_300km = 16 # €/mois
Abonnement_EZ_Drive_600km = 29 # €/mois

Emission_CO2 = np.zeros(10)
Guadeloupe = 0
Guyane = 1
La_Reunion = 2
Martinique = 3
Hexagone = 4
Ste_Lucie = 5
Mayotte = 6
Nouvelle_caledonie = 7
Polynesie = 8
L_essence = 9

Emission_CO2[0] = 0.7 # kgCO2/kWh
Emission_CO2[1] = 0.8 # kgCO2/kWh
Emission_CO2[2] = 0.78 # kgCO2/kWh
Emission_CO2[3] = 0.84 # kgCO2/kWh
Emission_CO2[4] = 0.07 # kgCO2/kWh
Emission_CO2[5] = 0.78 # kgCO2/kWh
Emission_CO2[6] = 0.78 # kgCO2/kWh
Emission_CO2[7] = 0.69 # kgCO2/kWh
Emission_CO2[8] = 0.57 # kgCO2/kWh
Emission_CO2[9] = 2.34 # kgCO2/L


NbreVS = 3 #Donnée à prendre dans les inputs clients#VS:vehicule salarie
NbreVU = 1 #Donnée à prendre dans les inputs clients#VS:vehicule utilitaire
NbkmanVS = 10000 #Donnée à prendre dans les inputs clients
NbkmanVU = 12000#Donnée à prendre dans les inputs clients
Presenceparking = True #Donnée à prendre dans les inputs clients
Accessibilite_parking = "Public" #Donnée à prendre dans les inputs clients
Optionborne = True #Donnée à prendre dans les inputs clients
Territoire = Martinique #Donnée à prendre dans les inputs clients
Nb_pdc_choisi = 2 #Donnée à prendre dans les inputs clients

Cout_vehicule_thermique_annuel = np.ones((5,20))
Cout_vehicule_thermique_annuel[0,0] = 12*(Prix_vehicule_thermique*NbreVS+Prix_utililaire_thermique*NbreVU)
Cout_vehicule_thermique_annuel[1,0] = Prix_carburant_initial
Cout_vehicule_thermique_annuel[2,0] = (NbreVS*NbkmanVS*Consommation_vehicule_thermique+NbreVU*NbkmanVU*Consommation_utilitaire_thermique)/100*Cout_vehicule_thermique_annuel[1,0]
Cout_vehicule_thermique_annuel[3,0] = Cout_vehicule_thermique_annuel[2,0]/Cout_vehicule_thermique_annuel[1,0]
Cout_vehicule_thermique_annuel[4,0] = Cout_vehicule_thermique_annuel[0,0] + Cout_vehicule_thermique_annuel[2,0]

for i in range (1,20):
    Cout_vehicule_thermique_annuel[0,i] = 12*(Prix_vehicule_thermique*NbreVS+Prix_utililaire_thermique*NbreVU)
    Cout_vehicule_thermique_annuel[1,i] = Cout_vehicule_thermique_annuel[1,i-1] * (1 + Augmentation_prix_carburant)
    Cout_vehicule_thermique_annuel[2,i] = (NbreVS*NbkmanVS*Consommation_vehicule_thermique+NbreVU*NbkmanVU*Consommation_utilitaire_thermique)/100*Cout_vehicule_thermique_annuel[1,i]
    Cout_vehicule_thermique_annuel[3,i] = Cout_vehicule_thermique_annuel[2,i]/Cout_vehicule_thermique_annuel[1,i]
    Cout_vehicule_thermique_annuel[4,i] = Cout_vehicule_thermique_annuel[0,i] + Cout_vehicule_thermique_annuel[2,i]
 
Cout_vehicule_electrique_annuel = np.ones((4,20))
Cout_vehicule_electrique_annuel[0,0] = 12*(Prix_vehicule_electrique*NbreVS+Prix_utililaire_electrique*NbreVU)
Cout_vehicule_electrique_annuel[1,0] = Prix_electricite
Cout_vehicule_electrique_annuel[2,0] = (NbreVS*NbkmanVS*Consommation_vehicule_electrique+NbreVU*NbkmanVU*Consommation_utilitaire_electrique)/100*Cout_vehicule_electrique_annuel[1,0]
Cout_vehicule_electrique_annuel[3,0] = Cout_vehicule_electrique_annuel[0,0] + Cout_vehicule_electrique_annuel[2,0]

for i in range (1,20):
    Cout_vehicule_electrique_annuel[0,i] = 12*(Prix_vehicule_electrique*NbreVS+Prix_utililaire_electrique*NbreVU)
    Cout_vehicule_electrique_annuel[1,i] = Cout_vehicule_electrique_annuel[1,i-1] * (1 + Augmentation_prix_electricite)
    Cout_vehicule_electrique_annuel[2,i] = (NbreVS*NbkmanVS*Consommation_vehicule_electrique +NbreVU*NbkmanVU*Consommation_utilitaire_electrique)/100*Cout_vehicule_electrique_annuel[1,i]
    Cout_vehicule_electrique_annuel[3,i] = Cout_vehicule_electrique_annuel[0,i] + Cout_vehicule_electrique_annuel[2,i]

Investissement_bornes = np.zeros(4)
Nb_borne_double = 0
Nb_borne_simple = 0

if Presenceparking:
    if Optionborne:
        Nb_borne_double = Nb_pdc_choisi//2
        Nb_borne_simple = Nb_pdc_choisi % 2
        
if Optionborne:
    if Accessibilite_parking == "Public":
        Investissement_bornes[0] = Nb_borne_double * Investissement_initial_borne_double_PUBLIC + Nb_borne_simple * Investissement_initial_borne_simple_PUBLIC
        Investissement_bornes[1] = Nb_borne_double * Prix_borne_double_PUBLIC + Nb_borne_simple * Prix_borne_simple_PUBLIC
    else:
        Investissement_bornes[0] = Nb_borne_double * Investissement_initial_borne_double_PRIVATE + Nb_borne_simple * Investissement_initial_borne_simple_PRIVATE
        Investissement_bornes[1] = Nb_borne_double * Prix_borne_double_PRIVATE + Nb_borne_simple * Prix_borne_simple_PRIVATE

Investissement_bornes[2] = Investissement_bornes[0] + Investissement_bornes[1] * 12 * 5

if Optionborne and Accessibilite_parking == "Public":
    Investissement_bornes[3] = Benefice_revente_elec * Estim_conso_borne * 365 * Nb_pdc_choisi
    
Abonnement_EZ_Drive_salarié = 0
Abonnement_EZ_Drive_utilitaire = 0

if not Optionborne:
    if NbkmanVS / 12 < 150 :
        Abonnement_EZ_Drive_salarié = NbreVS * Abonnement_EZ_Drive_150km
    elif NbkmanVS / 12 < 300 :
        Abonnement_EZ_Drive_salarié = NbreVS * Abonnement_EZ_Drive_300km
    else:
        Abonnement_EZ_Drive_salarié = NbreVS * Abonnement_EZ_Drive_600km
        
    if NbkmanVU / 12 < 150 :
        Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_150km
    elif NbkmanVU / 12 < 300 :
        Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_300km
    else:
        Abonnement_EZ_Drive_utilitaire = NbreVU * Abonnement_EZ_Drive_600km

Bornes = np.zeros((3,20))

for i in range (20):
    Bornes[0,i] = Investissement_bornes[1]*12
    if i%5 == 0:
        Bornes[0,i] += Investissement_bornes[0]
    Bornes[1,i] = Investissement_bornes[3]
    Bornes[2,i] = (Abonnement_EZ_Drive_salarié + Abonnement_EZ_Drive_utilitaire) * 12
    
Differenciel_bornes = np.zeros((3,20)) #Thermique - electrique

for i in range (20):
    Differenciel_bornes[0,i] = Cout_vehicule_thermique_annuel[0,i] - Cout_vehicule_electrique_annuel[0,i] 
    Differenciel_bornes[1,i] = Cout_vehicule_thermique_annuel[2,i] - Cout_vehicule_electrique_annuel[2,i]
    Differenciel_bornes[2,i] = Cout_vehicule_thermique_annuel[4,i] - Cout_vehicule_electrique_annuel[3,i] - Bornes[0,i] + Bornes[1,i] - Bornes[2,i]
    
Bilan_mobilité = np.zeros((2,3))

Bilan_mobilité[0,0] = Differenciel_bornes[2,0]
Bilan_mobilité[0,1] = sum(Differenciel_bornes[2,:10])
Bilan_mobilité[0,2] = sum(Differenciel_bornes[2,])

Bilan_mobilité[1,0] = (NbkmanVS * NbreVS * Consommation_vehicule_thermique + NbreVU * NbkmanVU * Consommation_utilitaire_thermique) / 100 * Emission_CO2[9] - ((NbkmanVS * NbreVS * Consommation_vehicule_electrique + NbreVU * NbkmanVU * Consommation_utilitaire_electrique) / 100 * Emission_CO2[Territoire])
Bilan_mobilité[1,1] = Bilan_mobilité[1,0] * 10
Bilan_mobilité[1,2] = Bilan_mobilité[1,0] * 20
    
    