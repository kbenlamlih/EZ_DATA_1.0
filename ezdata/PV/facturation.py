from .models import ( ModulesPV, Taxe, Modules_factu,BDD, Taxe,Onduleurs, Monitoring, Main_doeuvre, Tableaux, Cables, Cheminement, Divers, Inge,Structure, )
from django.db.models import Sum

#Le but de cette classe est de définir les modules nécessaires à la facturation du client
#Il ya des objets fixes et des objets dynamiques, en fonction des réponses du client
#Variables statiques pour les tests
panneau= 'SUNERGX-HALF CUT 375'
surface = 18.49
puissance_centrale = 3.8
N=88
nb_module = 10
rqt = BDD.objects.get(N=88)
curseur = 1 #?? que veut dire le curseur de marge

#Definition de la marge en fonction de la taille de la centrale : sans revente de surplus !! A CHANGER
def marge(taille, installation):
   if installation== 'Monophasée':
        val= 0.5 * curseur
   else:
       if (taille<35):
            val= 0.45*curseur
       #if (taille<35):
            #val= 0.4 *curseur
       if(taille>35):
            val = 0.3 *curseur
       #if(taille>35):
          #  val = 0.25 *curseur
       #else :
           # val= 0
       return val

def nb_KACO(N):
    rqt = BDD.objects.get(N=N)
    Onduleurs = [rqt.Onduleur_1, rqt.Onduleur_2, rqt.Onduleur_3]
    n=0
    for i in Onduleurs:
        if 'KACO' in i:
            n= n+1
    return n

def nb_SUN(N):
    rqt = BDD.objects.get(N=N)
    Onduleurs = [rqt.Onduleur_1, rqt.Onduleur_2, rqt.Onduleur_3]
    n=0
    for i in Onduleurs:
        if 'SUN' in i:
            n= n+1
    return n

def nb_SUNG_50kW(N):
    rqt = BDD.objects.get(N=N)
    Onduleurs = [rqt.Onduleur_1, rqt.Onduleur_2, rqt.Onduleur_3]
    n=0
    for i in Onduleurs:
        if 'SUNGROW TL3 50kW' in i:
            n= n+1
    return n

def nb_ATON(N):
    rqt = BDD.objects.get(N=N)
    Onduleurs = [rqt.Onduleur_1,rqt.Batterie_1, rqt.Onduleur_2, rqt.Onduleur_3]
    n=0
    for i in Onduleurs:
        if 'SUNGROW TL3 50kW' in i:
            n= n+1
    return n

#Creer une liste d'onduleurs, si + qu'un

#Modules photovoltaiques
#Dans un premier temps on recupere les objets qui nous intéresse de la base de donnée pour remplir les données de la facturation

def calcu_prix(taille, toiture, territo, installation, N):
#Recuperer les équipements nécessaires a la centrale :

    l= []
    rqt0 = BDD.objects.get(N=N)
    Onduleurs_liste = [rqt0.Onduleur_1, rqt0.Onduleur_2, rqt0.Onduleur_3]
   # print(Onduleurs_liste)
    kaco=nb_KACO(N)
    sun=nb_SUN(N)
    sun_50=nb_SUNG_50kW(N)
    aton=nb_ATON(N)
    rqt_taxe= Taxe.objects.get(territ=territo)

    marge1= marge(taille, installation)

    #Modules Photovoltaiques
    rqt1= ModulesPV.objects.get(Nom=panneau)
    a = Modules_factu(module = rqt1.Nom, qt= nb_module,cout_unitaire= rqt1.Cout, cout_unitaire_transport= (rqt_taxe.transport_2*rqt1.Cout)/100,
    cout_total= nb_module*rqt1.Cout, cout_total_transport= nb_module*(rqt_taxe.transport_2*rqt1.Cout)/100,marge=(nb_module*rqt1.Cout * marge1),
    prix= nb_module*rqt1.Cout+nb_module*(rqt_taxe.transport_2*rqt1.Cout)/100+(nb_module*rqt1.Cout * marge1),prix_unitaire= ( nb_module*rqt1.Cout+nb_module*(rqt_taxe.transport_2*rqt1.Cout)/100+(nb_module*rqt1.Cout * marge1))/nb_module)

    a.save()
    l.append(a)
    rqt2= Divers.objects.get(model='Eco participation')
    b = Modules_factu(module = rqt2.model, qt= nb_module,cout_unitaire= rqt2.cout, cout_unitaire_transport= 0,
    cout_total= nb_module*rqt2.cout, cout_total_transport=0 ,marge=(nb_module*rqt2.cout * marge1),
    prix= nb_module*rqt2.cout+(nb_module*rqt2.cout * marge1),prix_unitaire= ( nb_module*rqt2.cout+(nb_module*rqt2.cout * marge1))/nb_module)

    b.save()
    l.append(b)

    #Fixation rail
    if taille < 10:
        if (toiture== 'Tôle bac acier trapézoïdal'):
            rqt3= Structure.objects.get(model ='Fixation sur toiture bac acier trapézoïdal<10kW')
        if (toiture == 'Terrasse'):
            rqt3=Structure.objects.get(model= 'Fixation sur toiture terrasse<10kW')
    else:
        if (toiture== 'Tôle bac acier trapézoïdal'):
            rqt3= Structure.objects.get(model ='Fixation sur toiture bac acier trapézoïdal>10kW')
        if (toiture == 'Terrasse'):
            rqt3=Structure.objects.get(model= 'Fixation sur toiture terrasse>10kW')

    qt1= taille*1000
    c = Modules_factu(module = rqt3.model, qt= qt1,cout_unitaire= rqt3.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt3.cout)/100,
    cout_total= qt1*rqt3.cout, cout_total_transport= qt1*(rqt_taxe.transport_3*rqt3.cout)/100,marge=(qt1*rqt3.cout * marge1),
    prix= qt1*rqt3.cout+qt1*(rqt_taxe.transport_3*rqt3.cout)/100+(qt1*rqt3.cout * marge1),prix_unitaire= (qt1*rqt3.cout+qt1*(rqt_taxe.transport_3*rqt3.cout)/100+(qt1*rqt3.cout * marge1))/qt1)

    c.save()
    l.append(c)

    #Lestage
    rqt4= Structure.objects.get(model='Leste 25kg')
    if toiture== 'Terrasse':
        qt2= nb_module*3

        d = Modules_factu(module = rqt4.model, qt= qt2,cout_unitaire= rqt4.cout, cout_unitaire_transport= 0,
        cout_total= qt2*rqt4.cout, cout_total_transport= 0,marge=(qt2*rqt4.cout * marge1),
        prix= qt2*rqt4.cout+(qt2*rqt4.cout * marge1),prix_unitaire= (qt2*rqt4.cout+(qt2*rqt4.cout * marge1))/qt2)

        d.save()
        l.append(d)
    #onduleurs

    for i in Onduleurs_liste:
        if i!= '':
          # print(i)
            rqt5= Onduleurs.objects.get(model=i)
           # print(rqt5.model)
           # print('ok')

            e = Modules_factu(module = rqt5.model, qt= 1,cout_unitaire= rqt5.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt5.cout)/100,
            cout_total= 1*rqt5.cout, cout_total_transport= 1*(rqt_taxe.transport_3*rqt5.cout)/100,marge=(1*rqt5.cout * marge1),
            prix= 1*rqt5.cout+1*(rqt_taxe.transport_3*rqt5.cout)/100+(1*rqt5.cout * marge1),prix_unitaire= ( 1*rqt5.cout+1*(rqt_taxe.transport_3*rqt5.cout)/100+(1*rqt5.cout * marge1))/1)

            e.save()
            l.append(e)
        else:
            pass

    #Monitoring

    if (installation=='Triphasée'):
        if (taille<18.5):
            rqt9= Monitoring.objects.get(model='Solar log base 15 + extension')
        if (18.5 < taille < 101):
            rqt9=  Monitoring.objects.get(model='Solar log base 100')
        if (taille>=101):
            rqt9 =  Monitoring.objects.get(model='Solar log base 2000')
    if (installation=='Monophasée'):
         rqt9 =  Monitoring.objects.get(model='Solar log base 15 + extension')

    if aton>=1:
        qt3=0
    else:
        qt3=1
        f = Modules_factu(module = rqt9.model, qt= 1,cout_unitaire= rqt9.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt9.cout)/100,
        cout_total= 1*rqt9.cout, cout_total_transport= (rqt_taxe.transport_3*rqt9.cout)/100,marge=(1*rqt9.cout * marge1),
        prix= 1*rqt9.cout+1*(rqt_taxe.transport_3*rqt9.cout)/100+(1*rqt9.cout * marge1),prix_unitaire= (1*rqt9.cout+1*(rqt_taxe.transport_3*rqt9.cout)/100+(1*rqt9.cout * marge1))/1)

        f.save()
        l.append(f)

        rqt6= Monitoring.objects.get(model='Compteur non intrusif') #Compteur non intrusif
        rqt7 = Monitoring.objects.get(model='Tore de comptage 200 A')

        g = Modules_factu(module = rqt6.model, qt= 1,cout_unitaire= rqt6.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt6.cout)/100,
        cout_total= 1*rqt6.cout, cout_total_transport= 1*(rqt_taxe.transport_3*rqt6.cout)/100,marge=(1*rqt6.cout * marge1),
        prix= 1*rqt6.cout+1*(rqt_taxe.transport_3*rqt6.cout)/100+(1*rqt6.cout * marge1),prix_unitaire= (1*rqt6.cout+1*(rqt_taxe.transport_3*rqt6.cout)/100+(1*rqt6.cout * marge1))/1)

        g.save()
        l.append(g)

        h = Modules_factu(module = rqt7.model, qt= 1,cout_unitaire= rqt7.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt7.cout)/100,
        cout_total= 1*rqt7.cout, cout_total_transport= 1*(rqt_taxe.transport_3*rqt7.cout)/100,marge=(1*rqt7.cout * marge1),
        prix= 1*rqt7.cout+1*(rqt_taxe.transport_3*rqt7.cout)/100+(1*rqt7.cout * marge1),prix_unitaire= (1*rqt7.cout+1*(rqt_taxe.transport_3*rqt7.cout)/100+(1*rqt7.cout * marge1))/1)

        h.save()
        l.append(h)

        rqt8= Monitoring.objects.get(model='Alimentation sur prise électrique')

        j = Modules_factu(module = rqt8.model, qt= 1,cout_unitaire= rqt8.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt8.cout)/100,
        cout_total= 1*rqt8.cout, cout_total_transport= 1*(rqt_taxe.transport_3*rqt8.cout)/100,marge=(1*rqt8.cout * marge1),
        prix= 1*rqt8.cout+1*(rqt_taxe.transport_3*rqt8.cout)/100+(1*rqt8.cout * marge1),prix_unitaire= (1*rqt8.cout+1*(rqt_taxe.transport_3*rqt8.cout)/100+(1*rqt8.cout * marge1))/1)

        j.save()
        l.append(j)


    #Tableaux
    if (installation=="Triphasée"):
        if (kaco+sun>0) and (taille<61):
            if (taille<10):
                rqt10= Tableaux.objects.get(model= 'Coffret de protection AC 10kW')
            if (taille>=10):
                rqt10=  Tableaux.objects.get(model= 'Coffret de protection AC 60k')

            k = Modules_factu(module = rqt10.model, qt= 1,cout_unitaire= rqt10.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt10.cout, cout_total_transport= 0,marge=(1*rqt10.cout * marge1),
            prix= 1*rqt10.cout+(1*rqt10.cout * marge1),prix_unitaire= (1*rqt10.cout+(1*rqt10.cout * marge1))/1)

            k.save()
            l.append(k)

            rqt11= Tableaux.objects.get(model= 'Coffret de protection AC 80k')
        if (kaco+sun>0) and (taille>61):
            if (taille<10):
                rqt11= Tableaux.objects.get(model= 'Coffret de protection AC 80k')
            if (taille>=10):
                rqt11=  Tableaux.objects.get(model= 'Coffret de protection AC 100k')

            m = Modules_factu(module = rqt11.model, qt= 1,cout_unitaire= rqt11.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt11.cout, cout_total_transport= 0,marge=(1*rqt11.cout * marge1),
            prix= 1*rqt11.cout+(1*rqt11.cout * marge1),prix_unitaire= (1*rqt11.cout+(1*rqt11.cout * marge1))/1)

            m.save()
            l.append(m)
        rqt12= Tableaux.objects.get(model= 'Coffret de protection DC')

        n = Modules_factu(module = rqt12.model, qt= 1,cout_unitaire= rqt12.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt12.cout, cout_total_transport= 0,marge=(1*rqt12.cout * marge1),
            prix= 1*rqt12.cout+(1*rqt12.cout * marge1),prix_unitaire= (1*rqt12.cout+(1*rqt12.cout * marge1))/1)

        n.save()
        l.append(n)

        if aton>=1:
            rqt13= Tableaux.objects.get(model= 'EPS Box Triphasé')
            o = Modules_factu(module = rqt13.model, qt= 1,cout_unitaire= rqt13.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt13.cout)/100,
                cout_total= 1*rqt13.cout, cout_total_transport= 1*(rqt_taxe.transport_3*rqt13.cout)/100,marge=(1*rqt13.cout * marge1),
                prix= 1*rqt13.cout+(1*rqt13.cout * marge1)+1*(rqt_taxe.transport_3*rqt13.cout)/100,prix_unitaire= (1*rqt13.cout+1*(rqt_taxe.transport_3*rqt13.cout)/100+(1*rqt13.cout * marge1))/1)

            o.save()
            l.append(o)

        if (taille<85):
            if (taille<17):
                rqt14= Tableaux.objects.get(model= "Général d'injection solaire 25A")
            if (17<taille<43):
                rqt14= Tableaux.objects.get(model= "Général d'injection solaire 63A avec VIGI")
            if (taille>=43):
                rqt14= Tableaux.objects.get(model= "Général d'injection solaire 125A avec VIGI")
            p = Modules_factu(module = rqt14.model, qt= 1,cout_unitaire= rqt14.cout, cout_unitaire_transport= 0,
                cout_total= 1*rqt14.cout, cout_total_transport= 0,marge=(1*rqt14.cout * marge1),
                prix= 1*rqt14.cout+(1*rqt14.cout * marge1),prix_unitaire= (1*rqt14.cout+(1*rqt14.cout * marge1))/1)

            p.save()
            l.append(p)

        if (taille>85):
            if (taille<172):
                rqt15= Tableaux.objects.get(model= "Général d'injection solaire 160A avec VIGI")
            if (taille>=172):
                rqt15= Tableaux.objects.get(model= "Général d'injection solaire 1000A avec VIGI")

            q = Modules_factu(module = rqt15.model, qt= 1,cout_unitaire= rqt15.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt15.cout)/100,
                cout_total= 1*rqt15.cout, cout_total_transport= 1*(rqt_taxe.transport_3*rqt15.cout)/100,marge=(1*rqt15.cout * marge1),
                prix= 1*rqt15.cout+(rqt_taxe.transport_3*rqt15.cout)/100+(1*rqt15.cout * marge1),prix_unitaire= (1*rqt15.cout+(rqt_taxe.transport_3*rqt15.cout)/100+(1*rqt15.cout * marge1))/1)

            q.save()
            l.append(q)
    else:
        if (kaco+sun>0) and (taille<6,5):
            rqt10= Tableaux.objects.get(model= 'Coffret de protection AC 6,5k')

            k = Modules_factu(module = rqt10.model, qt= 1,cout_unitaire= rqt10.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt10.cout, cout_total_transport= 0,marge=(1*rqt10.cout * marge1),
            prix= 1*rqt10.cout+(1*rqt10.cout * marge1),prix_unitaire= (1*rqt10.cout+(1*rqt10.cout * marge1))/1)

            k.save()
            l.append(k)
        if (kaco+sun>0) and (taille>6,5):
            rqt11= Tableaux.objects.get(model= 'Coffret de protection AC 10kW')

            m = Modules_factu(module = rqt11.model, qt= 1,cout_unitaire= rqt11.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt11.cout, cout_total_transport= 0,marge=(1*rqt11.cout * marge1),
            prix= 1*rqt11.cout+(1*rqt11.cout * marge1),prix_unitaire= (1*rqt11.cout+(1*rqt11.cout * marge1))/1)

            m.save()
            l.append(m)
        rqt12= Tableaux.objects.get(model= 'Coffret de protection DC')

        qt5= kaco*sun
        n = Modules_factu(module = rqt12.model, qt= qt5,cout_unitaire= rqt12.cout, cout_unitaire_transport= 0,
            cout_total= qt5*rqt12.cout, cout_total_transport= 0,marge=(qt5*rqt12.cout * marge1),
            prix= qt5*rqt12.cout+(qt5*rqt12.cout * marge1),prix_unitaire= (qt5*rqt12.cout+(qt5*rqt12.cout * marge1))/qt5)

        n.save()
        l.append(n)
        if(taille<6,5):
            rqt13= Tableaux.objects.get(model= "Général d'injection solaire 25A")

            p1 = Modules_factu(module = rqt13.model, qt= 1,cout_unitaire= rqt13.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt13.cout, cout_total_transport= 0,marge=(1*rqt13.cout * marge1),
            prix= 1*rqt13.cout+(1*rqt13.cout * marge1),prix_unitaire= (1*rqt13.cout+(1*rqt13.cout * marge1))/1)

            p1.save()
            l.append(p1)
        if(taille>6,5):
            rqt14= Tableaux.objects.get(model= "Général d'injection solaire 63A avec VIGI")

            p = Modules_factu(module = rqt14.model, qt= 1,cout_unitaire= rqt14.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt14.cout, cout_total_transport= 0,marge=(1*rqt14.cout * marge1),
            prix= 1*rqt14.cout+(1*rqt14.cout * marge1),prix_unitaire= (1*rqt14.cout+(1*rqt14.cout * marge1))/1)

            p.save()
            l.append(p)

        if(rqt0.Onduleur_1=='ATON 3K MONO'):
            rqt15= Tableaux.objects.get(model= 'EPS Box Monophasé 3k')
            q = Modules_factu(module = rqt15.model, qt= 1,cout_unitaire= rqt15.cout, cout_unitaire_transport= 0,
            cout_total= 1*rqt15.cout, cout_total_transport= 0,marge=(1*rqt15.cout * marge1),
            prix= 1*rqt15.cout+(1*rqt15.cout * marge1),prix_unitaire= (1*rqt15.cout+(1*rqt15.cout * marge1))/1)

            q.save()
            l.append(q)

        else:
            if ( 'ATON' in rqt0.Onduleur_1):

                rqt16= Tableaux.objects.get(model= 'EPS Box Monophasé 4k 5k')
                r = Modules_factu(module = rqt16.model, qt= 1,cout_unitaire= rqt16.cout, cout_unitaire_transport= 0,
                cout_total= 1*rqt16.cout, cout_total_transport= 0,marge=(1*rqt16.cout * marge1),
                prix= 1*rqt16.cout+(1*rqt16.cout * marge1),prix_unitaire= (1*rqt16.cout+(1*rqt16.cout * marge1))/1)

                r.save()
                l.append(r)
            if (rqt0.Batterie_1!= ''):
        #QEAC
                rqt17=  Tableaux.objects.get(model= "QEAC")
                s = Modules_factu(module = rqt17.model, qt= 1,cout_unitaire= rqt17.cout, cout_unitaire_transport= 0,
                cout_total= 1*rqt17.cout, cout_total_transport= 0,marge=(1*rqt17.cout * marge1),
                prix= 1*rqt17.cout+(1*rqt17.cout * marge1),prix_unitaire= (1*rqt17.cout+(1*rqt17.cout * marge1))/1)

                s.save()
                l.append(s)

    #Cables

    if (installation=="Triphasée"):
        #quantité du cable solaire PV100f pour triphasé
        qt6= round( 50+(taille-3.45)*15.2,-1)
        #quantité du cable FTP pour le triphasée
        qt7=100
        #quantité du cable cuivre nu 25 mm2 pour les triphasée
        qt8=round(30+(taille-3.45)*1.8, -1)
        if (taille<50):
            if (taille<15):
                rqt17= Cables.objects.get(model="Câble de raccordement 5G10")
                s = Modules_factu(module = rqt17.model, qt= 30,cout_unitaire= rqt17.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt17.cout)/100,
                    cout_total= 30*rqt17.cout, cout_total_transport= 30*(rqt_taxe.transport_3*rqt17.cout)/100,marge=(30*rqt17.cout * marge1),
                    prix= 30*rqt17.cout+30*(rqt_taxe.transport_3*rqt17.cout)/100+(30*rqt17.cout * marge1),prix_unitaire= (30*rqt17.cout+30*(rqt_taxe.transport_3*rqt17.cout)/100+(30*rqt17.cout * marge1))/30)

                s.save()
                l.append(s)
            if (taille>=15) :
                rqt17= Cables.objects.get(model="Câble de raccordement 5G16")
                s = Modules_factu(module = rqt17.model, qt= 1,cout_unitaire= rqt17.cout, cout_unitaire_transport= 0,
                cout_total= 1*rqt17.cout, cout_total_transport= 0,marge=(1*rqt17.cout * marge1),
                prix= 1*rqt17.cout+(1*rqt17.cout * marge1),prix_unitaire= (1*rqt17.cout+(1*rqt17.cout * marge1))/1)

                s.save()
                l.append(s)
        if (taille>50):
            rqt17= Cables.objects.get(model="Câble de raccordement 5G25")
            s = Modules_factu(module = rqt17.model, qt= 1,cout_unitaire= rqt17.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt17.cout)/100,
            cout_total= 1*rqt17.cout, cout_total_transport= (rqt_taxe.transport_3*rqt17.cout)/100,marge=(1*rqt17.cout * marge1),
            prix= 1*rqt17.cout+(rqt_taxe.transport_3*rqt17.cout)/100+(1*rqt17.cout * marge1),prix_unitaire= (1*rqt17.cout+(rqt_taxe.transport_3*rqt17.cout)/100+(1*rqt17.cout * marge1))/1)

            s.save()
            l.append(s)
    else:
        qt7=50

        if(taille<4):
             rqt17= Cables.objects.get(model="Câble de raccordement 3G2,5")
             s = Modules_factu(module = rqt17.model, qt= 30,cout_unitaire= rqt17.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt17.cout)/100,
                        cout_total= 30*rqt17.cout, cout_total_transport= 30*(rqt_taxe.transport_3*rqt17.cout)/100,marge=(30*rqt17.cout * marge1),
                        prix= 30*rqt17.cout+30*(rqt_taxe.transport_3*rqt17.cout)/100+(30*rqt17.cout * marge1),prix_unitaire= (30*rqt17.cout+30*(rqt_taxe.transport_3*rqt17.cout)/100+(30*rqt17.cout * marge1))/30)

             s.save()
             l.append(s)
        if (taille>=4):
            rqt17= Cables.objects.get(model="Câble de raccordement 3G10")
            s = Modules_factu(module = rqt17.model, qt= 30,cout_unitaire= rqt17.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt17.cout)/100,
                    cout_total= 30*rqt17.cout, cout_total_transport= 30*(rqt_taxe.transport_3*rqt17.cout)/100,marge=(30*rqt17.cout * marge1),
                    prix= 30*rqt17.cout+30*(rqt_taxe.transport_3*rqt17.cout)/100+(30*rqt17.cout * marge1),prix_unitaire= (30*rqt17.cout+30*(rqt_taxe.transport_3*rqt17.cout)/100+(30*rqt17.cout * marge1))/30)

            s.save()
            l.append(s)
        if (taille<5):
            qt6=50
            qt8=30
        if (5<taille<6.5):
            qt6=100
            qt8=50
        if (6.5<taille<10):
            qt8=60
        if (taille>10):
            qt8=75
        if (taille>6.5):
            qt6=150

    rqt18= Cables.objects.get(model="Câble solaire PV1000F 6mm²")
    q = Modules_factu(module = rqt18.model, qt= qt6,cout_unitaire= rqt18.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt18.cout)/100,
            cout_total= qt6*rqt18.cout, cout_total_transport= qt6*(rqt_taxe.transport_3*rqt18.cout)/100,marge=(qt6*rqt18.cout * marge1),
            prix= qt6*rqt18.cout+qt6*(rqt_taxe.transport_3*rqt18.cout)/100+(qt6*rqt18.cout * marge1),prix_unitaire= (qt6*rqt18.cout+qt6*(rqt_taxe.transport_3*rqt18.cout)/100+(qt6*rqt18.cout * marge1))/qt6)

    q.save()
    l.append(q)

    rqt19= Cables.objects.get(model="Câble V/J 6mm²")
    r = Modules_factu(module = rqt19.model, qt= 15,cout_unitaire= rqt19.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt19.cout)/100,
            cout_total= 15*rqt19.cout, cout_total_transport= 15*(rqt_taxe.transport_1*rqt19.cout)/100,marge=(15*rqt19.cout * marge1),
            prix= 15*rqt19.cout+15*(rqt_taxe.transport_1*rqt19.cout)/100+(15*rqt19.cout * marge1),prix_unitaire= (15*rqt19.cout+15*(rqt_taxe.transport_1*rqt19.cout)/100+(15*rqt19.cout * marge1))/15)

    r.save()
    l.append(r)
    
    rqt20= Cables.objects.get(model="Terragrif, MC4, bornier bi metal")
 
    
    t = Modules_factu(module = rqt20.model, qt= qt1,cout_unitaire= rqt20.cout, cout_unitaire_transport= (rqt_taxe.transport_3*rqt20.cout)/100,
    cout_total= qt1*rqt20.cout, cout_total_transport= qt1*(rqt_taxe.transport_3*rqt20.cout)/100,marge=(qt1*rqt20.cout * marge1),
    prix= qt1*rqt20.cout+qt1*(rqt_taxe.transport_3*rqt20.cout)/100+(qt1*rqt20.cout * marge1),prix_unitaire= (qt1*rqt20.cout+qt1*(rqt_taxe.transport_3*rqt20.cout)/100+(qt1*rqt20.cout * marge1))/qt1)

    t.save()
    l.append(t)

    rqt21= Cables.objects.get(model="Câble FTP")
    u = Modules_factu(module = rqt21.model, qt= qt7,cout_unitaire= rqt21.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt21.cout)/100,
    cout_total= qt7*rqt21.cout, cout_total_transport= qt7*(rqt_taxe.transport_1*rqt21.cout)/100,marge=(qt7*rqt21.cout * marge1),
    prix= qt7*rqt21.cout+qt7*(rqt_taxe.transport_1*rqt21.cout)/100+(qt7*rqt21.cout * marge1),prix_unitaire= (qt7*rqt21.cout+qt7*(rqt_taxe.transport_1*rqt21.cout)/100+(qt7*rqt21.cout * marge1))/qt7)

    u.save()
    l.append(u)

    rqt22= Cables.objects.get(model="Câble Cuivre nu 25 mm²")
    v = Modules_factu(module = rqt22.model, qt= qt8,cout_unitaire= rqt22.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt22.cout)/100,
    cout_total= qt8*rqt22.cout, cout_total_transport= qt8*(rqt_taxe.transport_1*rqt22.cout)/100,marge=(qt8*rqt22.cout * marge1),
    prix= qt8*rqt22.cout+qt8*(rqt_taxe.transport_1*rqt22.cout)/100+(qt8*rqt22.cout * marge1),prix_unitaire= (qt8*rqt22.cout+qt8*(rqt_taxe.transport_1*rqt22.cout)/100+(qt8*rqt22.cout * marge1))/qt8)

    v.save()
    l.append(v)
    #Cheminement
    if (installation=="Triphasée"):
        rqt23= Cheminement.objects.get(model="Cablofil 150")
        rqt24= Cheminement.objects.get(model="Console pour cablofil ")
        y = Modules_factu(module = rqt24.model, qt= 30,cout_unitaire= rqt24.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt24.cout)/100,
                    cout_total= 30*rqt24.cout, cout_total_transport= 30*(rqt_taxe.transport_1*rqt24.cout)/100,marge=(30*rqt24.cout * marge1),
                    prix= 30*rqt24.cout+30*(rqt_taxe.transport_1*rqt24.cout)/100+(30*rqt24.cout * marge1),prix_unitaire= (30*rqt24.cout+30*(rqt_taxe.transport_1*rqt24.cout)/100+(30*rqt24.cout * marge1))/30)

        y.save()
        l.append(y)
        if (taille<10):
            qt9=50
        if (10<taille<40):
            qt9=100
        if (40<taille<70):
            qt9=150
        if (10<taille<100):
            qt9=200
        if (taille>=100):
            qt9=300
    else:
        rqt23= Cheminement.objects.get(model="Goulotte 60x40")
        qt9=50
        
    w = Modules_factu(module = rqt23.model, qt= 30,cout_unitaire= rqt23.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt23.cout)/100,
                    cout_total= 30*rqt23.cout, cout_total_transport= 30*(rqt_taxe.transport_1*rqt24.cout)/100,marge=(30*rqt23.cout * marge1),
                    prix= 30*rqt23.cout+30*(rqt_taxe.transport_1*rqt24.cout)/100+(30*rqt23.cout * marge1),prix_unitaire= (30*rqt23.cout+30*(rqt_taxe.transport_1*rqt24.cout)/100+(30*rqt23.cout * marge1))/30)

    w.save()
    l.append(w)

    rqt25= Cheminement.objects.get(model="Gaine anti-UV")
    x = Modules_factu(module = rqt25.model, qt= qt9,cout_unitaire= rqt25.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt25.cout)/100,
    cout_total= qt9*rqt25.cout, cout_total_transport= qt9*(rqt_taxe.transport_1*rqt25.cout)/100,marge=(qt9*rqt25.cout * marge1),
    prix= qt9*rqt25.cout+qt9*(rqt_taxe.transport_1*rqt25.cout)/100+(qt9*rqt25.cout * marge1),prix_unitaire= (qt9*rqt25.cout+qt9*(rqt_taxe.transport_1*rqt25.cout)/100+(qt9*rqt25.cout * marge1))/qt9)

    x.save()
    l.append(x)

    
    if (toiture== 'Tôle bac acier trapézoïdal'):
        if (taille <10):
            rqt26= Main_doeuvre.objects.get(model="Pose PV toiture tôle + Raccordement < 10kWc")
        if (10 < taille < 50):
            rqt26= Main_doeuvre.objects.get(model="Pose PV toiture tôle + Raccordement < 50kWc")
        if(taille>50):
             rqt26= Main_doeuvre.objects.get(model="Pose PV toiture tôle + Raccordement > 50kWc")

    if (toiture == 'Terrasse'):
        if (taille <10):
            rqt26= Main_doeuvre.objects.get(model="Pose PV toiture terrasse + Raccordement < 10kWc")
        if (10 < taille < 50):
            rqt26= Main_doeuvre.objects.get(model="Pose PV toiture terrasse + Raccordement < 50kWc")
        else:
             rqt26= Main_doeuvre.objects.get(model="Pose PV toiture terrasse + Raccordement > 50kWc")
             
    c1 = Modules_factu(module = rqt26.model, qt= qt1,cout_unitaire= rqt26.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt26.cout)/100,
    cout_total= qt1*rqt26.cout, cout_total_transport= qt1*(rqt_taxe.transport_1*rqt26.cout)/100,marge=(qt1*rqt26.cout * marge1),
    prix= qt1*rqt26.cout+qt1*(rqt_taxe.transport_1*rqt26.cout)/100+(qt1*rqt26.cout * marge1),prix_unitaire= (qt1*rqt26.cout+qt1*(rqt_taxe.transport_1*rqt26.cout)/100+(qt1*rqt26.cout * marge1))/qt1)

    c1.save()
    l.append(c1)        

    if (installation=='Triphasée'):
        if (taille <50):
            rqt27= Main_doeuvre.objects.get(model="Grutage < 50kWc")
            if (taille>35):
                rqt28= Main_doeuvre.objects.get(model="Sécurisation < 50kWc")
                d1 = Modules_factu(module = rqt28.model, qt= 1,cout_unitaire= rqt28.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt28.cout)/100,
                cout_total= 1*rqt28.cout, cout_total_transport= 1*(rqt_taxe.transport_1*rqt28.cout)/100,marge=(1*rqt28.cout * marge1),
                prix= 1*rqt28.cout+1*(rqt_taxe.transport_1*rqt28.cout)/100+(1*rqt28.cout * marge1),prix_unitaire= (1*rqt28.cout+1*(rqt_taxe.transport_1*rqt28.cout)/100+(1*rqt28.cout * marge1))/1)

                d1.save()
                l.append(d1)
        if (taille>=50) :
            rqt27= Main_doeuvre.objects.get(model="Grutage > 50kWc")
            if (taille>35):
                rqt28= Main_doeuvre.objects.get(model="Sécurisation > 50kWc")

                d1 = Modules_factu(module = rqt28.model, qt= 1,cout_unitaire= rqt28.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt28.cout)/100,
                cout_total= 1*rqt28.cout, cout_total_transport= 1*(rqt_taxe.transport_1*rqt28.cout)/100,marge=(1*rqt28.cout * marge1),
                prix= 1*rqt28.cout+1*(rqt_taxe.transport_1*rqt28.cout)/100+(1*rqt28.cout * marge1),prix_unitaire= (1*rqt28.cout+1*(rqt_taxe.transport_1*rqt28.cout)/100+(1*rqt28.cout * marge1))/1)

                d1.save()
                l.append(d1)
        if (taille<10):
            rqt29= Divers.objects.get(model= 'APAVE installation < 10kWc')
        if(taille>=10):
            rqt29= Divers.objects.get(model= 'APAVE installation >=10kWc')



        e1 = Modules_factu(module = rqt27.model, qt= 1,cout_unitaire= rqt27.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt27.cout)/100,
        cout_total= 1*rqt27.cout, cout_total_transport= 1*(rqt_taxe.transport_1*rqt27.cout)/100,marge=(1*rqt27.cout * marge1),
        prix= 1*rqt27.cout+1*(rqt_taxe.transport_1*rqt27.cout)/100+(1*rqt27.cout * marge1),prix_unitaire= (1*rqt27.cout+1*(rqt_taxe.transport_1*rqt27.cout)/100+(1*rqt27.cout * marge1))/1)

        e1.save()
        l.append(e1)


    if (installation=="Monophasée"):
        rqt29= Divers.objects.get(model= 'CONSUEL')

    f1 = Modules_factu(module = rqt29.model, qt= 1,cout_unitaire= rqt29.cout, cout_unitaire_transport= (rqt_taxe.transport_1*rqt29.cout)/100,
        cout_total= 1*rqt29.cout, cout_total_transport= 1*(rqt_taxe.transport_1*rqt29.cout)/100,marge=(1*rqt29.cout * marge1),
        prix= 1*rqt29.cout+1*(rqt_taxe.transport_1*rqt29.cout)/100+(1*rqt29.cout * marge1),prix_unitaire= (1*rqt29.cout+1*(rqt_taxe.transport_1*rqt29.cout)/100+(1*rqt29.cout * marge1))/1)

    f1.save()
    l.append(f1)

# Calculs de taxes pour chaque requette

    return l

def total_HA(taille, toiture, territo, installation, N):
    c = Modules_factu.objects.aggregate(Sum('cout_total'))
    a= c['cout_total__sum']
    return a

def total_Transport(taille, toiture, territo, installation, N):
    c = Modules_factu.objects.aggregate(Sum('cout_total_transport'))
    a= c['cout_total_transport__sum']

    return a

def total_Marge(taille, toiture, territo, installation, N):
    c = Modules_factu.objects.aggregate(Sum('marge'))
    a= c['marge__sum']
    return a

def total_prix(taille, toiture, territo, installation, N):
    c = Modules_factu.objects.aggregate(Sum('prix'))
    a= c['prix__sum']

    return a







