import numpy as np
import scipy as sc
from scipy.optimize import linprog as lin

"""
1er problème:

on pose:
- salaire : salaire à l'heure d'un employé | s = 12
- coût essence des machines trotoire /h    | gaz_t = 16 (8 l/h . 2 $/l)
- coût essence des machines route /h       | gaz_r = 20 (10 l/h . 2 $/l)
- coût maintenance machines par an         | m = 4.000 (rapporté à une journée: ~ 18$ /jour /machine)
- nb d'heure max (entre 5 et 8 am)         | nbh = 3
- vitesse machines trottoire               | v_t = 5 km/h
- vitesse machines route                   | v_r = 10 km/h
- durée globale: 180 jours (6 mois)
- durée travail par jour: 1h

On veut le nombre de machines de trotoire xt, le nombre de machines route xr, et le nombre d'employés xe,
sachant que xe = 2xr + xt

On cherche ainsi à minimiser les effectifs (xe, xt, xr) afin de rentrer dans le budget

FONCTION OBJECTIF: MIN z = 180*(10*xt + 16*xr + 20*xe)
  -> (s*xe + gaz_t*xt + gaz_r*xr) * nbJours
  -> z < 7M

CONTRAINTES:
- z <= 7.000.000
-          45xr >= 228  ---> nb km max parcourus par deneigneuse R x nb deneigeuse R
-    30xt       >= 449  ---> nb km max parcourus par deneigneuse T x nb deneigeuse T

-      xt + xr  <= 2200 ---> 220 appareils max
- xe            <= 3000 ---> 3000 employés max

- xe  = xt + 2xr        ---> 2 employés par machime R, 1 employé par machine T
"""
#-------------------------------------------------------------------------------------------
ze = 180 * 10
zt = 180 * 16
zr = 180 * 24

c = [ze, zt, zr]
A = [[ze, zt, zr], [0, -100, -150], [0, -1, 0], [0, 0, -1], [1, 0, 0], [0, 1, 2]]
b = [7000000, -136000, -90, -28, 3000, 2200]
Aeq = [[1, -1, -2]]
beq = [0]


sol1 = lin(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, method='simplex', options={"disp": True})
#-------------------------------------------------------------------------------------------

"""
resultats: 1374 employés, 1318 MT, 28 MR, budget = 6.39M$

On remarque une différence conséquente entre
le nombre de MT et le nombre de MR. Il faut trouver
une autre solution.
"""
#___________________________________________________________________________________________
#-------------------------------------------------------------------------------------------
#___________________________________________________________________________________________

"""
2ème solution

Le nombre de MT doit être égal à 2x le nombre de MR
On cherche toujours à minimiser le coût
"""

#-------------------------------------------------------------------------------------------
ze = 180 * 10
zt = 180 * 16
zr = 180 * 20

c = [ze, zt, zr]
A = [[ze, zt, zr], [0, -100, -150], [0, -1, 0], [0, 0, -1], [1, 0, 0], [0, 1, 2]]
b = [7000000, -136000, -90, -28, 3000, 2200]
Aeq = [[1, -1, -2], [0, 1, -2]]
beq = [0, 0]


sol2 = lin(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, method='simplex', options={"disp": True})
#-------------------------------------------------------------------------------------------

"""
resultats: 1554 employés, 778 MT, 338 MR, budget = 6.44 M$

Nous avons pensé à deux améliorations partant de ces résultats.

La première est la maximisation du budget, donc maximiser les xe, xt et xr
de telle manière à ce qu'on utilise complètement les 7M de budget
"""

#-------------------------------------------------------------------------------------------
ze = 180 * 10
zt = 180 * 16
zr = 180 * 20

c = [-ze, -zt, -zr]
A = [[ze, zt, zr], [0, -100, -150], [0, -1, 0], [0, 0, -1], [1, 0, 0], [0, 1, 2]]
b = [7000000, -136000, -90, -28, 3000, 2200]
Aeq = [[1, -1, -2], [0, 1, -2]]
beq = [0, 0]


sol2_1 = lin(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, method='simplex', options={"disp": True})
#-------------------------------------------------------------------------------------------

"""
La deuxième solution est d'utiliser la marge de 565.000$ tel que suit:
- 15.000$ pour les drones
- 550.000 pour la maintenance des machines.
"""










#-------------------------------------------------------------------------------------------
