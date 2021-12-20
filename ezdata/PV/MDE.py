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

Benefice_revente_elec= 0.05 # €/KWh
Estim_conso_borne = 40  # kWh/jour
Abonnement_EZDrive_150km = 9 # €/mois
Abonnement_EZ_Drive_300km= 16 # €/mois
Abonnement_EZ_Drive_600km= 29 # €/mois

Emission_CO2_Guadeloupe = 0.7 # CO2/kWh
Emission_CO2_Martinique = 0.84 # CO2/kWh
Emission_CO2_Guyane = 0.8 # CO2/kWh
Emission_CO2_Mayotte = 0.78 # CO2/kWh
Emission_CO2_Reunion = 0.78 # CO2/kWh
Emission_L_essence = 2.34 # CO2/kWh


NbrekWhfacture = 40000 #Donnée à prendre dans les inputs clients
Recurrencefacture = 'Mensuelle' #Donnée à prendre dans les inputs clients
Montantfacture = 8000 #Donnée à prendre dans les inputs clients

if Recurrencefacture == 'Mensuelle' :
    mois = 12
    
if Recurrencefacture == 'Bimestrielle' :
        mois = 6
    
if Recurrencefacture == 'Annuelle' :
        mois = 1

#print(mois)
    
NbrekWhannuel = NbrekWhfacture*mois
Montantannuel = Montantfacture*mois

Surfacetoiture = 2000 #Donnée à prendre dans les inputs clients
Nbreetages = 1 #Donnée à prendre dans les inputs clients

consokwhman = NbrekWhannuel/(Surfacetoiture*Nbreetages) #kWh/m²/an
consoeuroan = Montantannuel/(Surfacetoiture*Nbreetages) #euros/m²/an

prix_elec = Montantannuel/NbrekWhannuel #A aller chercher dans Inputs (dans cet onglet, le prix est déterminé soit en fonction de la facture si on l'a, soit en fonction du secteur si on a pas d'infos sur la facture)
augm_prix_elec = 2.5 #en %, à aller chercher dans 'Inputs'

BDD_Bat_ADB = [0] * 5
BDD_Bat_ADB[0]= 158.0000
BDD_Bat_ADB[1] = 114.0000
BDD_Bat_ADB[2]= 33.0000
BDD_Bat_ADB[3]= 24.0000
BDD_Bat_ADB[4]= BDD_Bat_ADB[1]/BDD_Bat_ADB[0] - 1

BDD_Bat_AB = [0] * 5
BDD_Bat_AB[0] = 198.0000
BDD_Bat_AB[1] = 158.0000
BDD_Bat_AB[2] = 64.0000
BDD_Bat_AB[3] = 48.0000
BDD_Bat_AB[4] = BDD_Bat_AB[1]/BDD_Bat_AB[0] - 1

BDD_Bat_AG = [0] * 5
BDD_Bat_AG[0] = 227.0000
BDD_Bat_AG[1] = 167.0000
BDD_Bat_AG[2] = 85.0000
BDD_Bat_AG[3] = 63.0000
BDD_Bat_AG[4] = BDD_Bat_AG[1]/BDD_Bat_AG[0] - 1

BDD_Bat_A = [0] * 5
BDD_Bat_A[0] = 227.0000
BDD_Bat_A[1] = 167.0000
BDD_Bat_A[2] = 85.0000
BDD_Bat_A[3] = 63.0000
BDD_Bat_A[4] = BDD_Bat_A[1]/BDD_Bat_A[0] - 1

BDD_Bat_BTP = [0] * 5
BDD_Bat_BTP[0] = 472
BDD_Bat_BTP[1] = 416
BDD_Bat_BTP[2] = 69
BDD_Bat_BTP[3] = 58
BDD_Bat_BTP[4] = BDD_Bat_BTP[1]/BDD_Bat_BTP[0] - 1

BDD_Bat_CHR = [0] * 5
BDD_Bat_CHR[0] = 130
BDD_Bat_CHR[1] = 112
BDD_Bat_CHR[2] = 18
BDD_Bat_CHR[3] = 14
BDD_Bat_CHR[4] = BDD_Bat_CHR[1]/BDD_Bat_CHR[0] - 1

BDD_Bat_CBE = [0] * 5
BDD_Bat_CBE[0] = 158
BDD_Bat_CBE[1] = 114
BDD_Bat_CBE[2] = 33
BDD_Bat_CBE[3] = 24
BDD_Bat_CBE[4] = BDD_Bat_CBE[1]/BDD_Bat_CBE[0] - 1

BDD_Bat_CNA = [0] * 5
BDD_Bat_CNA[0] = 158
BDD_Bat_CNA[1] = 125
BDD_Bat_CNA[2] = 33
BDD_Bat_CNA[3] = 24
BDD_Bat_CNA[4] = BDD_Bat_CNA[1]/BDD_Bat_CNA[0] - 1

BDD_Bat_GA = [0] * 5
BDD_Bat_GA[0] = 896
BDD_Bat_GA[1] = 668
BDD_Bat_GA[2] = 114
BDD_Bat_GA[3] = 85
BDD_Bat_GA[4] = BDD_Bat_GA[1]/BDD_Bat_GA[0] - 1

BDD_Bat_I = [0] * 5
BDD_Bat_I[0] = 472
BDD_Bat_I[1] = 416
BDD_Bat_I[2] = 69
BDD_Bat_I[3] = 58
BDD_Bat_I[4] = BDD_Bat_I[1]/BDD_Bat_I[0] - 1

BDD_Bat_M = [0] * 5
BDD_Bat_M[0] = 137
BDD_Bat_M[1] = 117
BDD_Bat_M[2] = 21
BDD_Bat_M[3] = 18
BDD_Bat_M[4] = BDD_Bat_M[1]/BDD_Bat_M[0] - 1

BDD_Bat_MB = [0] * 5
BDD_Bat_MB[0] = 500
BDD_Bat_MB[1] = 303
BDD_Bat_MB[2] = 96
BDD_Bat_MB[3] = 58
BDD_Bat_MB[4] = BDD_Bat_MB[1]/BDD_Bat_MB[0] - 1

BDD_Bat_PMA = [0] * 5
BDD_Bat_PMA[0] = 500
BDD_Bat_PMA[1] = 303
BDD_Bat_PMA[2] = 96
BDD_Bat_PMA[3] = 58
BDD_Bat_PMA[4] = BDD_Bat_PMA[1]/BDD_Bat_PMA[0] - 1

BDD_Bat_S = [0] * 5
BDD_Bat_S[0] = 225
BDD_Bat_S[1] = 160
BDD_Bat_S[2] = 36
BDD_Bat_S[3] = 25
BDD_Bat_S[4] = BDD_Bat_S[1]/BDD_Bat_S[0] - 1

BDD_Bat_T = [0] * 5
BDD_Bat_T[0] = 3245
BDD_Bat_T[1] = 2936
BDD_Bat_T[2] = 934
BDD_Bat_T[3] = 862
BDD_Bat_T[4] = BDD_Bat_T[1]/BDD_Bat_T[0] - 1


#print (BDD_Bat_ADB)
#print (BDD_Bat_AB)
#print (BDD_Bat_AG)
#print (BDD_Bat_A)
#print (BDD_Bat_BTP)
#print (BDD_Bat_CHR)
#print (BDD_Bat_CBE)
#print (BDD_Bat_CNA)
#print (BDD_Bat_GA)
#print (BDD_Bat_I)
#print (BDD_Bat_M)
#print (BDD_Bat_MB)
#print (BDD_Bat_PMA)
#print (BDD_Bat_S)
#print (BDD_Bat_T)


type_batiment = 'AB' #Doit aller chercher ce que le client entre en input

if type_batiment == 'ADB' :
    type_bat = BDD_Bat_ADB

if type_batiment == 'AB' :
    type_bat = BDD_Bat_AB 
    
if type_batiment == 'AG' :
    type_bat = BDD_Bat_AG

if type_batiment == 'A' :
    type_bat = BDD_Bat_A
    
if type_batiment == 'BTP' :
    type_bat = BDD_Bat_BTP

if type_batiment == 'CHR' :
    type_bat = BDD_Bat_CHR
    
if type_batiment == 'CBE' :
    type_bat = BDD_Bat_CBE

if type_batiment == 'CNA' :
    type_bat = BDD_Bat_CNA
        
if type_batiment == 'GA' :
    type_bat = BDD_Bat_GA

if type_batiment == 'I' :
    type_bat = BDD_Bat_I
    
if type_batiment == 'M' :
    type_bat = BDD_Bat_M

if type_batiment == 'MB' :
    type_bat = BDD_Bat_MB
        
if type_batiment == 'PMA' :
    type_bat = BDD_Bat_PMA

if type_batiment == 'S' :
    type_bat = BDD_Bat_S
    
if type_batiment == 'T' :
    type_bat = BDD_Bat_T
   
  
    
if consokwhman < type_bat[2] :
    reduc = 0.05
if consokwhman > type_bat[2] :
    reduc_possible = -1*type_bat[4]
    #print (reduc_possible)
#On veut que la réduction soit entrée automatiquement par l'outil et ne plus avoir besoin d'opé comme actuellement
   
    if reduc_possible > .10 and reduc_possible < .15 :
        reduc = 0.06
    if reduc_possible > .15 and reduc_possible < .20 :
        reduc = 0.07
    if reduc_possible > .20 and reduc_possible < .25 :
        reduc = 0.08
    if reduc_possible > .25 and reduc_possible < .30 :
        reduc = 0.09    
    if reduc_possible > 30 :
        reduc = 0.1 

print (reduc*100, "%")
#print (type_bat)

#Tableau de consommation d'électricité annuelle :

ancienne_conso = [NbrekWhannuel]*20
#print (ancienne_conso)

conso_reduite = [NbrekWhannuel*(1-reduc)]*20
#print (conso_reduite)

tab_prix_elec = [0] *20
tab_prix_elec[0] = prix_elec
for i in range(1, 20) :
    prix_elec = prix_elec*(1+augm_prix_elec/100)
    tab_prix_elec[i] = prix_elec
    
#print (tab_prix_elec)

difference = [0] * 20
for i in range(20) :
    difference[i] = (ancienne_conso[i] - conso_reduite[i]) * tab_prix_elec[i]

#print (difference)
    
tableau_conso_MDE = [ancienne_conso, conso_reduite, tab_prix_elec, difference]
print (tableau_conso_MDE)

#Bilan : Economies réalisables MDE
Bilan_Economique = [0]*3
Bilan_Economique[0] = difference[0]
Bilan_Economique[1] = 0

for k in range(10) :
    Bilan_Economique[1] += difference[k]
Bilan_Economique[2] = sum(difference)

Bilan_Energétique = [0]*3
Bilan_Energétique[0] = ancienne_conso[0] - conso_reduite[0]
Bilan_Energétique[1] = Bilan_Energétique[0] *10
Bilan_Energétique[2] = Bilan_Energétique[0] *20

hyp_emissions_CO2 = 0.84 #A aller chercher dans INPUT et dépend du territoire
Bilan_Environnemental = [0] * 3
Bilan_Environnemental[0] = Bilan_Energétique[0]*hyp_emissions_CO2
Bilan_Environnemental[1] = Bilan_Energétique[1]*hyp_emissions_CO2
Bilan_Environnemental[2] = Bilan_Energétique[2]*hyp_emissions_CO2

Bilan_Eco_MDE = [Bilan_Economique, Bilan_Energétique, Bilan_Environnemental]
print (Bilan_Eco_MDE)


#Investissement MDE
taux_invest = 0.1 #Pourcentage des économies sur 20 ans qui finance la MDE
invest = taux_invest * Bilan_Economique[2]

print (invest)
