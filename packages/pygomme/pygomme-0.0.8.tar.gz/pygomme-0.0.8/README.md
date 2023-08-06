# Pygomme 

**Premier exemple : utilisation de mesures expérimentales**



<pre><code>
import pygomme as pg
import numpy as np  

"""
Premier exemple : Type A

Création d'un objet pygomme.MeasureA à partir de données expérimentales (bidonnées)
L'utilisateur indique la fonction de distribution qu'il veut utiliser. Celle-ci aura la même moyenne et le même écart-type que les données.
"""
measures = [4.534e3,4.524e3,4.555e3,4.566e3,4.514e3,4.508e3,4.535e3,4.507e3,
            4.534e3,4.574e3,4.576e3,4.535e3,4.584e3,4.594e3,4.524e3,4.556e3,]

re = pg.MeasureA(label="R/\Omega",       # label utilisé uniquement pour les graphiques
                title="Résistance $R$",  # idem
                experimental_data=measures, # listes des mesures (doit être itérables)  
                distribution=np.random.normal, # fonction de distribution utilisée
                )

re.histogram(n=int(1e5),    # Nombre de points utilisés pour le graphique
             file="Re-normal.png", # Nom du fichier graphique créé
             )

"""
Utilisation des mêmes données, mais avec une autre fonction de distribution.
"""
re.distribution = np.random.uniform # fonction de distribution utilisée

re.histogram(n=int(1e6),    # Nombre de points utilisés pour le graphique
             file="Re-uniform.png", # Nom du fichier graphique créé
             )

"""
Mesure de la vitesse du son. Exemple emprunté à M. Champion
"""

d = np.array([10, 13, 17, 20, 22, 26, 30, 33, 37, 40 ])*1e-2
tau = np.array([0.27, 0.38, 0.50, 0.59, 0.66, 0.73, 0.90, 0.96, 1.09, 1.15])*1e-3

c_exp = d/tau

c = pg.MeasureA(label="\\frac{c}{m/s}",
                title="Vitesse des ondes sonores",
                experimental_data=c_exp,
                )

print(f"La vitesse des ondes est {c} m/s.")

c.histogram(file="Celerite-1.png")

"""
Utilisation d'un second jeux de données.
"""
c.experimental_data = np.array([343.8, 339.2, 343.0, 343.9, 
                                340.5, 335.8, 344.3, 341.0, 
                                346.5, 337.9, 345])

c.histogram(file="Celerite-2.png")

print(f"La vitesse des ondes est {c} m/s.")
</code></pre>

**Second exemple : Type B et propagation.**

<pre><code>
#!/usr/bin/env python3
"""
Second exemple : Type B et propagation.

Création de plusieurs objets pygomme.MeasureB, avec différentes fonctions de distribution.
Création de deux objets pygomme.Propagation pour étudier la propagation des erreurs en utilisant la méthode CdL.
"""
import pygomme as pg
import numpy as np  

r1 = pg.MeasureB(label="R_1/\Omega",      # label pour les graphiques
                title="Résistance $R_1$", # idem
                value=9.8e3,              # valeur moyenne 
                half_width=0.2e3,         # demi-largeur de la distribution
                distribution=np.random.uniform, # choix d'une distribution uniforme
                )

r2 = pg.MeasureB(label="R_2/\Omega", 
                title="Résistance $R_2$",
                value=15.3e3,       # valeur moyenne
                scale=0.2e3,        # déviation standard 
                distribution = np.random.normal, # choix d'une loi normale
                )

# Création des fichiers contenant les courbes
r1.histogram(gaussian=True, # Affichage d'une gaussienne de même moyenne et écart-type
             n=int(1e4),  # Nombre de points pour l'histogramme
             file="R1-hist.png",  # Fichier de sortie
             )
r2.histogram(gaussian=True, n=int(1e4), file="R2-hist.png")

# Fonction ancillaire pour l'étude de la propagation des erreurs.
# Cette fonction doit être vectorisée et être utilisable avec des paramètres
# de type numpy.ndarray
def parallele(ra,rb):
    r = ra*rb/(ra+rb)
    return r

# 
rp = pg.Propagation(label="R_p/\Omega", # Utilisé pour le graphiques
                    title="Résistance $R_p$", # idem
                    function=parallele,  # fonction de propagation des erreurs
                    argument=[r1,r2],   # objets pygomme
                    n_sim=int(1e5),  # Nombre de points pour la simulation CdL
                    )

# Tracé d'une figure avec la distribution pour les deux résistances R1 et R2
# et pour la résistance de l'association parrallèle.
rp.histogram(file="Rp.png",
             gaussian=True)

# Les valeurs moyenne et l'écart-type de Rp sont accessibles :
print("La valeur moyenne de Rp est {:.0f} Ω".format(rp.average()))

print("L'écart-type de Rp est {:.0f} Ω".format(rp.deviation()))

# Mais on peut aussi utiliser directement la fonction print() :
print(rp)

# La méthode report permet de créer une figure avec l'histogramme
# de distribution des trois résistances.
rp.report(file="Rp.png")

#
# Propagation d'erreurs avec une grandeur de type A et une de type B
#
rpp = pg.Propagation(label="R_p'/\Omega", # Utilisé pour le graphiques
                    title="Résistance $R_p'$", # idem
                    function=parallele,  # fonction de propagation des erreurs
                    argument=[r1,r2],   # objets pygomme
                    n_sim=int(1e6),  # Nombre de points pour la simulation CdL
                    )

rpp.report(file="Rpp.png")
rpp.report_partial(file="Rpp-partial.png")

# On ajoute deux autres résisances.
r3 = pg.MeasureB(label="R_3/\Omega",
                title="Résistance $R_3$",
                value=12.5e3 ,
                half_width=0.5e3 ,
                distribution=np.random.triangular,)

r4 = pg.MeasureB(label = "R_4/\Omega",
                title="Résistance $R_4$",
                value = 11.3e3,
                scale = 0.4e3,
                distribution = np.random.normal,)

# Association des quatre résistances.
def parallele_serie(r1,r2,r3,r4):
    r = r1*r2/(r1+r2) + r3*r4/(r3+r4)
    return r

rps = pg.Propagation(label = "R_{ps}/\Omega",
                    title="Résistance $R_{ps}$",
                    function=parallele_serie,
                    argument=[r1,r2,r3,r4],
                    n_sim=int(1e5))

# Figure avec les histogrammes des cinq résistances.
rps.report(file="Rps.png")

# Figure qui permet d'évaluer l'influence des différents paramètres.
# Pour les quatre premières courbes, la simulation CdL est faite en n'utilisant
# que la distribution d'une des quatre résistances, les autres étant prises égales à
# leur valeur moyenne.
rps.report_partial(file="Rps-partial.png")

# Calcul et écriture de l'écart normalisé entre Rp et Rps:
print(rps-rp)
# que l'on utilisera correctement:
print("L'écart normalisé est {:.2f}".format(rps-rp))

# Création d'une grandeur de référence :
r_ref = pg.Reference(label = "R_{réf}/\Omega",
                     title="Résistance $R_{réf}$",
                     value=11.8e3)

# Affichage de l'écart normalisé entre Rps et R_ref :
print("L'écart normalisé est {:.2f}".format(rps-r_ref))

# Création d'un objet pygomme.Compare qui permet de comparer les 
# histogrammes de deux objets pygomme.
d = rps // r_ref
d.report(file="D-report.png",n=int(2e5))
d.report(file="D-report-lr.png",n=int(2e3))

# Création d'une nouvelle mesure Rt
rt = pg.MeasureB(label = "R_t/\Omega",
                title="Résistance $R_t$",
                value = 11.3e3 ,
                scale = 0.4e3 ,
                distribution = np.random.normal,
                )

# Calcul et écriture de l'écart normalisé entre Rps et Rt:
print(rps-rt)

# Création d'un objet pygomme.Compare
c = rps // rt
# une syntaxe équivalente : C = pg.Compare(A=Rps,B=Rt)
# 
# Affichage des histogrammes :
c.report(file="C-report.png",n=int(2e5))
c.report(file="C-report-lr.png",n=int(2e3))
</code></pre>

**Troisième exemple : Utilistation d'un multimètre. **

<pre><code>
#!/usr/bin/env python3
"""
Troisième exemple : Utilistation d'un multimètre.

La precision est donnée par le constructeur, avec en général, une contribution absolue (digit) et une contribution relative.
"""

import pygomme as pg
#import numpy as np  

u = pg.MeasureMultimeter(label="U/\mathrm{V}",   # pour les graphiques
                        title="Tension mesurée", # idem
                        value=5.184,             # valeur lue : 5.184 V 
                        precision_digit=8e-2,    # precision : 0.08 V
                        precision_relative=5e-3, # precision : 0.5 %
                        )

i = pg.MeasureMultimeter(label="I/\mathrm{A}",
                        title="Intensité mesurée",
                        value=0.1234,            # Valeur lue : 0.1234 A
                        precision_digit=10e-3,   # precision : 1 mA
                        precision_relative=1e-2) # precision : 1 % 

def ohm(u,i) :
    return u/i

r = pg.Propagation(label="R/\Omega",
                title="résistance $R$",
                function=ohm,
                argument=(u,i),
                n_sim = int(1e5))

# Création des graphiques
r.report(file="R-report.png")
r.report_partial(file="R-report_partial.png",gaussian=True)

</code></pre>

** Quatrième exemple : focométrie**

<pre><code>
#!/usr/bin/env python3
"""
Focométrie
"""

import numpy as np  
import pygomme as pg

xA = pg.MeasureB(label="x_A/m",
                title="Position de l'objet",
                value=0.112,
                half_width=2e-3,
                distribution=np.random.uniform,)

xAp = pg.MeasureB(label="x_A'/m",
                title="Position de l'image",
                value=1.122,
                half_width=2e-3,
                distribution=np.random.uniform,)

xO = pg.MeasureB(label="x_O/m",
                title="Position de la lentille",
                value=0.352,
                half_width=4e-3,
                distribution=np.random.uniform,)

def focometrie(xA,xAp,xO):
    fp = 1/(1/(xAp-xO)-1/(xA-xO))
    return fp

fp = pg.Propagation(label="f'/m",
                title="Distance focale",
                function=focometrie,
                argument=[xA,xAp,xO],
                n_sim=int(1e6))  

# Création des graphiques :
fp.report(file="Fp-report.png")
fp.report_partial(file="Fp-report_partial.png")

</code></pre>

** Calorimètrie **

<pre><code>
#!/usr/bin/env python3
"""
Calorimétrie

Exemple repris de 
https://www.ac-paris.fr/portail/jcms/p2_2334447/ressources-numeriques-mesures-et-incertitudes-bcpst-n1?cid=p1_2333951&portal=piapp1_59010
"""
import numpy as np  
import pygomme as pg

at = 0.1 # Demi-étendue pour les températures T1 et T2
atf = 1 # Demi-étendue pour la température Tf
am = 0.5 # Demi-étendue pour les masses

t1 = pg.MeasureB(label="T_1/°C",
                 title="Température de l'eau froide",
                 value=20.2,
                 half_width=at,
                 distribution=np.random.uniform)

t2 = pg.MeasureB(label="T_2/°C",
                 title="Température de l'eau chaude",
                 value=47.3,
                 half_width=at,
                 distribution=np.random.uniform)

tf = pg.MeasureB(label="T_f/°C",
                 title="Température finale",
                 value=31.2,
                 half_width=atf,
                 distribution=np.random.triangular)

m1i = pg.MeasureB(label="m_{1i}/\mathrm{g}",
                  title="Masse du bécher 1 plein",
                  value=153,
                  half_width=am,
                  distribution=np.random.uniform)

m1f = pg.MeasureB(label="m_{1f}/\mathrm{g}",
                  title="Masse du bécher 1 vide",
                  value=99,
                  half_width=am,
                  distribution=np.random.uniform)

m2i = pg.MeasureB(label="m_{2i}/\mathrm{g}",
                  title="Masse du bécher 2 plein",
                  value=176,
                  half_width=am,
                  distribution=np.random.uniform)

m2f = pg.MeasureB(label="m_{2f}/\mathrm{g}",
                  title="Masse du bécher 2 vide",
                  value=119,
                  half_width=am,
                  distribution=np.random.uniform)

def capacite(t1,t2,tf,m1i,m1f,m2i,m2f):
    c = 4.185*((m2i-m2f)*(t2-tf)/(tf-t1)+(m1f-m1i))
    return c

c_cal = pg.Propagation(label="C_{cal}/(J/K)",
                       title="Capacité thermique du calorimètre",
                       function=capacite,
                       argument=[t1,t2,tf,m1i,m1f,m2i,m2f],
                       n_sim = int(1e6),
                       )

c_cal.report("Ccal-report.png")
c_cal.report_partial("Ccal-report_partial.png")

</code></pre>

** Régression linéaire **

<pre><code>
#!/usr/bin/env python3
"""
Régression linéaire.

Exemple emprunté à Maxime Champion.
"""
import numpy as np  
import pygomme as pg

frequences = np.array([11.825,10.111,8.210,7.4129,6.8838])*100
u_frequences = np.array([2.3,1.7,1.1,0.91,0.79])

ec = np.array([2.40,1.69,0.91,0.57,0.35])
u_ec = 0.05

frequence = pg.MeasureB(label="\\frac{\\nu}{THz}",
                        title="Fréquence",
                        value=frequences,
                        scale =u_frequences,
                        distribution = np.random.normal,
                        )

energie = pg.MeasureB(label="\\frac{E_c}{eV}",
                      title="Énergie cinétique",
                      value=ec,
                      scale=u_ec,
                      distribution = np.random.normal,
                      )

lf = pg.LinearFit(x=frequence,
                  y=energie,
                  n=int(1e3))

print(lf)
print(lf.a)
print(lf.b)

lf.a.label = "a"
lf.a.histogram(file="a-hist.png")
lf.b.histogram(file="b-hist.png")
lf.report(file="Planck-report.png")

"""
Étude sans tenir compte de la corrélation entre a et b
"""

def constante_de_planck(a):
    h = a*1.602e-19*1e-12
    return h

def frequence_seuil(a,b):
    fs = -b/a
    return fs

h = pg.Propagation(label="h/(Js)",
                   title="Constante de Planck",
                   function=constante_de_planck,
                   argument=(lf.a,),
                   n_sim=int(1e5))

fs1 = pg.Propagation(label="\\frac{\\nu_1}{THz}",
                   title="Fréquence seuil sans corrélation",
                   function=frequence_seuil,
                   argument=(lf.a,lf.b),
                   n_sim=int(1e5))

h.histogram(file="h-hist.png")
fs1.report(file="fs-hist.png")

print(f"La constante de Planck est {h} J/s.")
print(f"La fréquence seuil est {fs1} THz.")

"""
Étude en tenant compte de la corrélation entre a et b
"""

ab = lf.ab
ab.a_label = "a"
ab.b_label = "b"
ab.scatter(file="ab-scatter.png")

fs_cor = -ab.b/ab.a

fs2 = pg.MeasureA(label="\\frac{\\nu_2}{THz}",     
                title="avec corrélation",  
                experimental_data=fs_cor, 
                distribution=np.random.normal,
                )

print(f"La fréquence seuil est {fs2} THz.")

cfs = fs1 // fs2

cfs.report(file="frequence-seuil-12.png")

"""
Étude en créant un objet pygomme.correlation
"""

data_a = lf.a.experimental_data
data_b = lf.b.experimental_data

ab2 = pg.Correlation(labels=["$a$","$b$"],
                titles=["pente","ordonnées à l'origine"],
                keys=['a','b'],
                color="gray",
                values=[data_a,data_b],)

ab2.compute_cov()

print(ab2.cov)

ab2.create_samples(n=int(1e5))

#print(ab2.samples['a'])

ab2.scatter(x=ab2.quantity['a'].samples(),
           y=ab2.quantity['b'].samples(),
           file="ab2-scatter.png")

def frequence_seuil(x,y):
    fs = -y/x
    return fs

fs3 = pg.Propagation(label="\\frac{\\nu_3}{THz}",
                   title="Fréquence seuil avec pygomme.correlation",
                   function=frequence_seuil,
                   argument=(ab2.quantity['a'],ab2.quantity['b']),
                   n_sim=int(1e6))

print(f"La fréquence seuil est {fs3} THz.")

cfs13 = fs1 // fs3

cfs13.report(file="frequence-seuil-13.png")

cfs23 = fs2 // fs3

cfs23.report(file="frequence-seuil-23.png")
</code></pre>
