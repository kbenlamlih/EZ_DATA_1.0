import numpy as np
from .models import Emisission_CO2, BDDBat,Hyp_cout_mobilite


rqt1= Hyp_cout_mobilite.objects.get(model="Augmentation prix électricité")
augm_prix_elec= rqt1.valeur
taux_invest = 0.1  # Pourcentage des économies sur 20 ans qui finance la MDE


#NbrekWhfacture = 40000  # Donnée à prendre dans les inputs clients
#Recurrencefacture = 'Mensuelle'  # Donnée à prendre dans les inputs clients
#Montantfacture = 8000  # Donnée à prendre dans les inputs clients
#Nbreetages = 1  # Donnée à prendre dans les inputs clients

def variables_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages ):

    if Recurrencefacture == 'Mensuelle':
        mois = 12

    if Recurrencefacture == 'Bimestrielle':
        mois = 6

    if Recurrencefacture == 'Annuelle':
        mois = 1


    NbrekWhannuel = NbrekWhfacture * mois
    Montantannuel = Montantfacture * mois


    consokwhman = NbrekWhannuel / (Surfacetoiture * Nbreetages)  # kWh/m²/an
    consoeuroan = Montantannuel / (Surfacetoiture * Nbreetages)  # euros/m²/an

    prix_elec = Montantannuel / NbrekWhannuel  # A aller chercher dans Inputs (dans cet onglet, le prix est déterminé soit en fonction de la facture si on l'a, soit en fonction du secteur si on a pas d'infos sur la facture)
    return consokwhman, consoeuroan, NbrekWhannuel, Montantannuel, prix_elec


def reduction(type, consokwhman):
    rqt0= BDDBat.objects.get(type=type)

    if consokwhman < rqt0.moy_euros_avant:
        reduc = 0.05
    if consokwhman > rqt0.moy_euros_avant:
        reduc_possible = -1 * rqt0.gain
        # print (reduc_possible)
        # On veut que la réduction soit entrée automatiquement par l'outil et ne plus avoir besoin d'opé comme actuellement

        if 0.10 < reduc_possible< 0.15:
            reduc = 0.06
        if 0.15 <= reduc_possible < 0.20:
            reduc = 0.07
        if 0.20 <= reduc_possible < 0.25:
            reduc = 0.08
        if  0.25 <= reduc_possible < 0.30:
            reduc = 0.09
        if reduc_possible >= 0.30:
            reduc = 0.1
    return reduc
# print (type_bat)

# Tableau de consommation d'électricité annuelle :

def coeffs_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages,type ):

    NbrekWhannuel= variables_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages )[2]
    consokwhman=variables_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages )[0]
    reduc= reduction(type,consokwhman)
    prix_elec= variables_mde(NbrekWhfacture,Recurrencefacture,Montantfacture, Surfacetoiture,Nbreetages )[4]

    ancienne_conso = [NbrekWhannuel] * 20
    ancienne_conso_coeff=[0] * 20
    # print (ancienne_conso)

    conso_reduite = [NbrekWhannuel * (1 - reduc)] * 20

    conso_reduite_coeff=[0] * 20
    # print (conso_reduite)

    tab_prix_elec = [0] * 20
    tab_prix_elec[0] = prix_elec
    for i in range(1, 20):
        prix_elec = prix_elec * (1 + augm_prix_elec / 100)
        tab_prix_elec[i] = prix_elec
        ancienne_conso_coeff[i] = ancienne_conso[i]*tab_prix_elec[i]
        conso_reduite_coeff[i] = conso_reduite[i]*tab_prix_elec[i]

        # print (tab_prix_elec)

    difference = [0] * 20
    for i in range(20):
        difference[i] = (ancienne_conso[i] - conso_reduite[i]) * tab_prix_elec[i]

    #tableau_conso_MDE = [ancienne_conso, conso_reduite, tab_prix_elec, difference]
    return ancienne_conso_coeff, conso_reduite_coeff, tab_prix_elec, difference, ancienne_conso,conso_reduite

# Bilan : Economies réalisables MDE
def Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type, territ):
    ancienne_conso= coeffs_mde(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type)[4]
    conso_reduite= coeffs_mde(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type)[5]
    difference = coeffs_mde(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type)[3]



    Bilan_Economique = [0] * 3
    Bilan_Economique[0] = round(difference[0],2)
    Bilan_Economique[1] = 0

    for k in range(10):
        Bilan_Economique[1] += difference[k]
    Bilan_Economique[1]=round(Bilan_Economique[1],2)
    Bilan_Economique[2] = round(sum(difference),2)

    Bilan_Energétique = [0] * 3
    Bilan_Energétique[0] = ancienne_conso[0] - conso_reduite[0]
    Bilan_Energétique[1] = Bilan_Energétique[0] * 10
    Bilan_Energétique[2] = Bilan_Energétique[0] * 20

    rqt= Emisission_CO2.objects.get(territ=territ)  # A aller chercher dans INPUT et dépend du territoire
    hyp_emissions_CO2 = rqt.emission


    Bilan_Environnemental = [0] * 3
    Bilan_Environnemental[0] = Bilan_Energétique[0] * hyp_emissions_CO2
    Bilan_Environnemental[1] = Bilan_Energétique[1] * hyp_emissions_CO2
    Bilan_Environnemental[2] = Bilan_Energétique[2] * hyp_emissions_CO2

    #Bilan_Eco_MDE = [Bilan_Economique, Bilan_Energétique, Bilan_Environnemental]
    return Bilan_Economique, Bilan_Energétique,Bilan_Environnemental

    # Investissement MDE
def Invest(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type,territ):
    Bilan_Economique= Economies(NbrekWhfacture, Recurrencefacture, Montantfacture, Surfacetoiture, Nbreetages, type,territ)[0]
    invest = taux_invest * Bilan_Economique[2]

    return invest