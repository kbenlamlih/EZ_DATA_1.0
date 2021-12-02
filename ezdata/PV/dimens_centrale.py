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
Estim_conso_borne =  40  # kWh/jour
Abonnement_EZDrive_150km = 9 # €/mois
Abonnement_EZ_Drive_300km= 16 # €/mois
Abonnement_EZ_Drive_600km= 29 # €/mois

Emission_CO2_Guadeloupe = 0.7 # CO2/kWh
Emission_CO2_Martinique = 0.84 # CO2/kWh
Emission_CO2_Guyane = 0.8 # CO2/kWh
Emission_CO2_Mayotte = 0.78 # CO2/kWh
Emission_CO2_Reunion = 0.78 # CO2/kWh
Emission_L_essence = 2.34 # CO2/kWh


PR= 0.81 #A modifier ?
Rendement_batteries_Lithium= 0.95
Decharge_maximale_batteries_Lithium = 0.8
Perte1 = 0.05 #%
Nb_jours_ouvres= 261
Nb_jours_favorables= 219
Ep_moyenne= 4 #kWh/kWc
Ep_defavorable= 2.5 #kWh/kWc
Ep_favorable= 5 #kWh/kWc


def conso(profil):
    if profil == 'Particulier':
        conso = 91.40
    if profil == 'Tertiaire':
        conso = 65.41
    if profil == 'Hôtel':
        conso = 112.68
    if profil == 'Personnalisé':
        conso = 72.85
    if profil == 'Mesuré':
        conso = 110.13
    if profil == 'Station':
        conso = 87.61
    if profil == 'Fastfood':
        conso = 100.88
    return conso

#Dimensonnement
def courbes_de_charges_coeff(profil):
    if profil == 'Particulier':
        coeffs_ouvre = np.matrix(
            [0.513002919254087, 0.513002919254087, 0.513002919254087, 0.513002919254087, 0.513002919254087,
             0.513002919254087, 0.513002919254087,
             0.573441598700519, 0.635308535824081, 0.513002919254087, 0.396796297915364, 0.330000000000000,
             0.300000000000000, 0.287648882196555,
             0.287648882196555, 0.300000000000000, 0.320000000000000, 0.380000000000000, 0.500000000000000,
             0.800000000000000, 0.900000000000000,
             0.730000000000000, 0.573441598700519, 0.513002919254087])

        coeffs_ouvre = coeffs_ouvre.transpose()

        coeffs_weekend = np.matrix(
            [0.510, 0.510, 0.510, 0.510, 0.510, 0.510, 0.510, 0.540, 0.600, 0.700, 0.680, 0.710, 0.813, 0.800, 0.700,
             0.630, 0.600, 0.630, 0.700,
             0.850, 1.000, 0.950, 0.780, 0.620])

        coeffs_weekend = coeffs_weekend.transpose()

    if profil == 'Tertiaire':
        coeffs_ouvre = np.matrix(
            [0.19314795, 0.180555997, 0.183323404, 0.187397552, 0.177793126, 0.187208889, 0.26648297, 0.498094031,
             0.705463615, 0.920881528,
             1, 0.929495464, 0.868438843, 0.8148189, 0.833076595, 0.831896015, 0.685177583, 0.444108783, 0.254105649,
             0.22104276,
             0.196684716, 0.18027861, 0.179813418, 0.180466512])

        coeffs_ouvre = coeffs_ouvre.transpose()

        coeffs_weekend = np.matrix(
            [0.170873567, 0.176385697, 0.184692055, 0.151749516, 0.146335958, 0.157185996, 0.165382372, 0.173627047,
             0.179149455, 0.226861686,
             0.272888662, 0.272888662, 0.275797822, 0.284546971, 0.281627006, 0.269983161, 0.230449165, 0.196562998,
             0.18191826, 0.179149455,
             0.190254382, 0.184692055, 0.176385697, 0.176385697])

        coeffs_weekend = coeffs_weekend.transpose()

    if profil == 'Hôtel':
        coeffs_ouvre = np.matrix(
            [0.49310741, 0.478460655, 0.430212522, 0.480470994, 0.4638139, 0.646754739, 0.682366456, 0.679207352,
             0.700459506, 0.753015508, 0.733486502, 0.703331419, 0.774267662,
             0.831131534, 0.731188972, 0.8552556, 0.853819644, 0.811889719, 1, 0.80987938, 0.707926479, 0.70591614,
             0.597932223, 0.581275129])

        coeffs_ouvre = coeffs_ouvre.transpose()

        coeffs_weekend = np.matrix(
            [0.44111143, 0.463325675, 0.449167145, 0.431835152, 0.453561172, 0.543394601, 0.543394601, 0.629078116,
             0.651048248, 0.674483056, 0.601493395, 0.760654796, 0.599296381,
             0.569026422, 0.704753016, 0.681318208, 0.776033889, 0.785798392, 0.716714532, 0.735999426, 0.74210224,
             0.668624354])

        coeffs_weekend = coeffs_weekend.transpose()



    if profil == 'Station':
        coeffs_ouvre = np.matrix(
            [0.192727273, 0.192727273, 0.192727273, 0.192727273, 0.192727273, 0.192727273, 0.289090909, 0.337272727,
             0.433636364, 0.770909091, 0.819090909, 0.867272727, 0.963636364,
             0.963636364, 0.963636364, 0.770909091, 0.770909091, 0.674545455, 0.722727273, 0.626363636, 0.385454545,
             0.385454545, 0.289090909, 0.192727273])

        coeffs_ouvre = coeffs_ouvre.transpose()

        coeffs_weekend = np.matrix(
            [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.35, 0.45, 0.8, 0.85, 0.9, 1, 1, 1, 0.8, 0.8, 0.7, 0.75, 0.65, 0.4,
             0.4, 0.3, 0.2])

        coeffs_weekend = coeffs_weekend.transpose()


    if profil == 'Fast Food':
        coeffs_ouvre = np.matrix(
            [0.294117647, 0.2, 0.176470588, 0.223529412, 0.188235294, 0.188235294, 0.176470588, 0.164705882,
             0.282352941, 0.847058824, 0.741176471, 0.858823529, 0.964705882, 0.929411765,
             0.964705882, 0.917647059, 0.847058824, 0.847058824, 0.917647059, 1, 0.905882353, 0.8, 0.635294118,
             0.341176471])

        coeffs_ouvre = coeffs_ouvre.transpose()

        coeffs_weekend = np.matrix(
            [0.294117647, 0.2, 0.176470588, 0.223529412, 0.188235294, 0.188235294, 0.176470588, 0.164705882,
             0.282352941, 0.847058824, 0.741176471, 0.858823529, 0.964705882, 0.929411765, 0.964705882,
             0.917647059, 0.847058824, 0.847058824, 0.917647059, 1, 0.905882353, 0.8, 0.635294118, 0.341176471])

        coeffs_weekend = coeffs_weekend.transpose()

    return (coeffs_ouvre, coeffs_weekend)


def courbe_de_charges(conso_perso, profil):
    conso_hebdo = conso(profil)
    coeffs_ouvre, coeffs_weekend = courbes_de_charges_coeff(profil)

    coeffs_ouvre = 1000 * (conso_perso / conso_hebdo) * coeffs_ouvre
    coeffs_weekend = 1000 * (conso_perso / conso_hebdo) * coeffs_weekend

    return coeffs_ouvre, coeffs_weekend

def courbe_irradiation (territ):
    if territ == 'Guadeloupe' or territ=='Martinique':
        hL = 6 #h
        So = 12 #h
        H_soleil = 5.41 #kWh/m2
        i=0
        #a= np.array([0,0,0])
        l=[]
    for i in range(23):
        #print(i)
        x=min(max(np.pi*(i-hL)/So,0),np.pi)
        #print(x)
        y=(np.sin(x)*np.pi)/(2*(So/24)*24)
        #print(y)
        z=y*H_soleil*1000*Ep_moyenne/4.35
        #print(z)
        l.append([x,y,z])
        i+=1
        #print(y)
    l = np.asarray(l)
        #b= np.array([x,y,z])
        #a1= np.append(a,[x,y,z], axis=0)
    return l

def pic_production (territ):
    if territ == 'Guadeloupe' or territ == 'Martinique':
        pic = max(courbe_irradiation(territ).max(axis=1))*PR/1000
    return pic #en kWc


def dimensionnement_potentiel_centrale_autoconso(conso_perso, profil, territ):  # conso en hebdo

    ouvre = courbe_de_charges(conso_perso, profil)[0]
    extract_ouvre = ouvre[10:15]
    total_extract_ouvre = np.sum(ouvre)
    # print(total_extract_ouvre)
    min_extract_ouvre = np.min(extract_ouvre)

    weekend = courbe_de_charges(conso_perso, profil)[1]
    extract_weekend = weekend[10:15]
    total_extract_weekend = np.sum(weekend)
    # print(total_extract_weekend)

    min_extract_weekend = np.min(extract_weekend)

    value = (min_extract_ouvre * total_extract_ouvre * 5 / conso_perso + min_extract_weekend * total_extract_weekend * 2 / conso_perso) / 1000 / 1000 / pic_production(territ)

    return value
    # resultat en kWc

