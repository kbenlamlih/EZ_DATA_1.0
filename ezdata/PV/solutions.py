# TABLEAU DES SOLUTIONS TRIPHASEES avec une ligne en plus = capacité de batterie // Mettre 0 pour les 4 premières colonnes
# Aller recuperer le numero de solution de la base de données SQL pour remplir le tableau de solution

from .models import BBD
from .models import ModulesPV
import numpy as np
from dimens_centrale import dimensionnement_potentiel_centrale_autoconso

surface_panneau = 0.375
puissance_panneau= 1.85

def tableau_solutions_triphase(installation, puissance):
    tab = np.zeros((38, 4), float)
    # REMPLISSAGE DU TABLEAU a la main des premieres valeurs : nb de modules / ligne des sans batterie

    tab[1][0] = 10
    tab[2][0] = 18
    tab[3][0] = 20
    tab[4][0] = 22
    tab[5][0] = 26
    tab[6][0] = 30
    tab[7][0] = 34
    tab[8][0] = 38
    tab[9][0] = 42
    tab[10][0] = 46
    tab[11][0] = 50
    tab[12][0] = 58
    tab[13][0] = 66
    tab[14][0] = 76
    tab[15][0] = 86
    tab[16][0] = 96
    tab[17][0] = 104
    tab[18][0] = 114
    tab[19][0] = 128
    tab[20][0] = 144
    tab[21][0] = 158
    tab[22][0] = 172
    tab[23][0] = 186
    tab[24][0] = 202
    tab[25][0] = 216
    tab[26][0] = 230
    tab[27][0] = 244
    tab[28][0] = 260
    tab[29][0] = 274
    tab[30][0] = 288
    tab[31][0] = 318
    tab[32][0] = 346
    tab[33][0] = 376
    tab[34][0] = 404
    tab[35][0] = 434
    tab[36][0] = 462
    tab[37][0] = 478

    for i in range(1, 38):
        for j in range(1, 4):
            if j == 1:
                tab[i][j] = (tab[i][0]) * surface_panneau

            if j == 2:
                tab[i][j] = (tab[i][0]) * puissance_panneau

            if j == 3:

                result = BDD.objects.filter (Electrical_installation=installation ).filter(Nb_modules_min <float(tab[i][0])).filter(Puissance_centrale_max>float(tab[i][2]))
                results = list()
                for r in result :
                    results.append((r.N, r.Prix_total_achat))

                # Prendre le numero de solution pour le prix d'achat le plus petit :

                if result:
                    t = min(result, key=lambda t: t[1])
                    tab[i][3] = t[0]
                else:
                    # prendre en compte les fois ou il n'y a pas de solutions
                    tab[i][3] = 0

    return tab


def solution_triphasee(conso_perso, profil, territ, surface, installation, puissance):
    # conso_perso= conso_moyenne*7

    # conso_moyenne = 115.07
    # profil = 'Tertiaire'
    # territ = 'Guadeloupe'

    # Rajouter condition si autoconso
    # if objectif = Optimiser autoco

    potentiel = dimensionnement_potentiel_centrale_autoconso(conso_perso, profil, territ)
    tab = tableau_solutions_triphase(installation, puissance)
    tab2 = np.zeros((38, 2), float)
    tab2[0][0] = 0
    tab2[0][1] = 0

    # Prendre en compte le cas ou pas de puissance souscrite = pas de facture EDF
    # if puissance = 0 :
    #puissance = 1000  # VA

    # surface = surface*0.96
    # surface = 192
    for i in range(1, 38):
        # print(i)
        tab2[i][0] = tab[i][2]
        if (tab[i][3] > 0 and tab[i][1] <= surface and tab[i][2] <= puissance + 1):
            tab2[i][1] = (1 - ((abs(potentiel - tab[i][2]) / max(potentiel, tab[i][2]) / 2)))
        else:
            tab2[i][1] = -1
    # print(tab2)
    result = tab2.argmax(axis=0)
    index = result[1]
    atteinte_potentiel = tab2[index][1]

    if atteinte_potentiel == 1:
        print("Aucune solution")

    # index= int(result[1])
    # print(tab2[index][index])

    return tab2[index][0], tab[index][3]


def solution_GT(conso_perso, profil, territ, surface, installation, puissance):
    centrale_GT = solution_triphasee(conso_perso, profil, territ, surface, installation, puissance)[0]
    numero_solution = solution_triphasee(conso_perso, profil, territ, surface, installation, puissance)[1]
    nbr_modules = centrale_GT / puissance_panneau
    surface_toiture = surface_panneau * nbr_modules

    rep = "La taille de la centrale proposé par GT est de " + str(centrale_GT) + "kWc. Elle est composé de " + str(
        nbr_modules) + " modules. Pour une surface totale de " + str(
        surface_toiture) + " m2.     Cela correspond à la solution " + str(numero_solution)

    return rep

#Création du tableau issu de la feuille Analyse de Production

def calcul_taux_centraleGT(conso_perso, profil, territ, surface,installation, puissance):
    centrale_GT = solution_triphasee(conso_perso, profil, territ, surface,installation, puissance)[0]
    coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0]
    coeffs_weekend = courbe_de_charges(conso_perso, profil)[1]

    G = courbe_irradiation('territ')
    tab = np.zeros((24, 8), float)

    for i in range(23):
        tab[i][0] = i  # Heures
        tab[i][1] = G[i][2] * PR * centrale_GT  # Energie produite moyenne (W)
        tab[i][2] = tab[i][1] * Ep_defavorable / Ep_moyenne  # Energie produite jour nuageux (Wh)
        tab[i][3] = tab[i][1] * Ep_favorable / Ep_moyenne  # Energie produite jour ensoleillé  (Wh)
        tab[i][4] = max(tab[i][2] - coeffs_ouvre[i], 0)  # Surplus jour ouvré nuageux  (Wh)
        tab[i][5] = max(tab[i][3] - coeffs_ouvre[i], 0)  # Surplus jour ouvré ensoleillé  (Wh)
        tab[i][6] = max(tab[i][2] - coeffs_weekend[i], 0)  # Surplus weekend nuageux  (Wh)
        tab[i][7] = max(tab[i][3] - coeffs_weekend[i], 0)  # Surplus weekend ensoleillé  (Wh)
        # print (tab[i][5])

    # Calcul de taux : a quoi ca sert????
    # Autoproduction
    autoconso_jour_ouvre_defavorable = (np.sum(tab[:, 2]) - np.sum(tab[:, 4])) / np.sum(
        tab[:, 2]) * 100  # Jour ouvré défavorable en prct
    autoconso_jour_ouvre_favorable = (np.sum(tab[:, 3]) - np.sum(tab[:, 5])) / np.sum(
        tab[:, 3]) * 100  # Jour ouvré favorable en prct
    autoconso_jour_weekend_defavorable = (np.sum(tab[:, 2]) - np.sum(tab[:, 6])) / np.sum(
        tab[:, 2]) * 100  # Weekend défavorable
    autoconso_jour_weekend_favorable = (np.sum(tab[:, 3]) - np.sum(tab[:, 7])) / np.sum(
        tab[:, 3]) * 100  # Weekend favorable

    # Taux final Annuel : totaux
    ep_ouvre_nuageux_annuel = np.sum(tab[:, 2]) * (365 - Nb_jours_favorables)
    ep_ouvre_soleil_annuel = np.sum(tab[:, 3]) * (Nb_jours_favorables)
    surplus_ouvre_nuageux_annuel = np.sum(tab[:, 4]) * (365 - Nb_jours_favorables) * Nb_jours_ouvres / 365
    surplus_ouvre_ensoleille_annuel = np.sum(tab[:, 5]) * Nb_jours_favorables * Nb_jours_ouvres / 365
    surplus_weekend_nuageux_annuel = np.sum(tab[:, 6]) * (365 - Nb_jours_favorables) * (365 - Nb_jours_ouvres) / 365
    surplus_weekend_ensoleille_annuel = np.sum(tab[:, 7]) * (365 - Nb_jours_ouvres) * Nb_jours_favorables / 365

    sum_charge_ouvre = np.sum(coeffs_ouvre) * Nb_jours_ouvres
    sum_charge_weekend = np.sum(coeffs_weekend) * (365 - Nb_jours_ouvres)

    taux_autoconso = (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel) / (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel) * 100

    taux_autoprod = (ep_ouvre_nuageux_annuel + ep_ouvre_soleil_annuel - surplus_ouvre_nuageux_annuel - surplus_ouvre_ensoleille_annuel - surplus_weekend_nuageux_annuel - surplus_weekend_ensoleille_annuel) / (sum_charge_ouvre + sum_charge_weekend) * 100
    return (tab, taux_autoconso, taux_autoprod)


# A la fin on retourne : taux_autoconso de la centrale + taux_autoprod
# return surplus_ouvre_ensoleille_annuel


def plot_courbes(conso_perso, profil):
    # Premier graphique : jour ouvré

    fig = plt.figure(1, figsize=(15, 5))

    coeffs_ouvre = courbe_de_charges(conso_perso, profil)[0] / 1000
    hours = ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00",
             "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    plt.title("PROFIL ENERGETIQUE : JOUR OUVRE MOYEN")

    plt.plot(hours, coeffs_ouvre, color='r', label="Courbe de charge")

    tab = calcul_taux_centraleGT()[0]
    result = tab[:, 1] / 1000

    # Surface pour l'energie PV consomé

    surface = np.zeros((24, 1), float)
    for i in range(24):
        surface[i] = min(result[i], coeffs_ouvre[i])
    surface = surface.flatten()

    plt.plot(hours, result, color='g', label="Production PV centrale proposée")

    plt.fill_between(hours, surface, color='#FFA500', label="Energie PV consommée")

    plt.legend()
    plt.show()

    # Deuxième graphique : weekend

    fig = plt.figure(2, figsize=(15, 5))

    coeffs_weekend = courbe_de_charges(115.07, 'Tertiaire')[1] / 1000
    plt.title("PROFIL ENERGETIQUE : WEEKEND MOYEN")

    plt.plot(hours, coeffs_weekend, color='r', label="Courbe de charge")
    tab = calcul_taux_centraleGT()[0]
    result = tab[:, 1] / 1000

    # Surface pour l'energie PV consomé

    surface = np.zeros((24, 1), float)
    for i in range(24):
        surface[i] = min(result[i], coeffs_weekend[i])
    surface = surface.flatten()

    plt.plot(hours, result, color='g', label="Production PV centrale proposée")

    plt.fill_between(hours, surface, color='#FFA500', label="Energie PV consommée")

    plt.legend()
    plt.show()
