#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Contient 'Gamma-Construction' & 'Vertex-Clique-Matrix-Construction'"""


import os
import random
import math
import datetime
import pickle

from decimal import Decimal
InFini = Decimal('Infinity')



TYPE = 'TYPE'               # 0 : type du sommet: 'P_node', 'Q_node', '?', 'Feuille'
FEP = 'FEP'                 # 1 : 'full' , 'empty', 'partial'  'pert' (pertinent)
ENS_F = 'ENS_F'             # 2 : ens des feuilles sous ce sommet (sert apres, sauf pour les feuilles)
PERE = 'PERE'               # 3 : pere
GD_FRERE = 'GD_FRERE'       # 4 : suivant (grand frere)
PTI_FRERE = 'PTI_FRERE'     # 5 : precedent (petit frere)
CADET = 'CADET'             # 6 : fils cadet
AINE = 'AINE'               # 7 : fils aine
NB_UN = 'NB_UN'             # 8 : nbre de un (ds la ligne traitee) en dessous de ce sommet

P_node = 'P_node'
Q_node = 'Q_node'
Feuille = 'Feuille'
full = 'full'
empty = 'empty'
partial = 'partial'
pert = 'pert'

TABLEAU_FEP = ['full', 'empty', 'partial'] # : les differentes valeurs (ds l'ordre) que que prendre FEP

## DEBUT CONSTRUCTION DISTANCES

def matrice_vide (nn) :
    matrice = []
    for i in range (nn) :
        matrice.append ([0]* nn)
    return matrice

def alea (jacta_est) :
    resultat = random.randint (0, abs(jacta_est))
    if jacta_est < 0 :
        resultat = round (resultat / abs(jacta_est))
    return resultat

def remplissage_Robinson (matrice, vecteur, jacta_est) :
    nn = len (vecteur)
    for diag in range (1, nn) :
        for i in range (nn - diag) :
            j = i + diag
            valeur_a_gauche = matrice [vecteur[i]][vecteur[j-1]]
            valeur_au_dessous = matrice[vecteur[i+1]][vecteur[j]]
            valeur = max (valeur_a_gauche, valeur_au_dessous) + alea (jacta_est)
            matrice[vecteur[i]][vecteur[j]] = valeur
    complementation (matrice)
    suppression_des_zeros (matrice)

def suppression_des_zeros (mat) :
    n = len (mat)
    for x in range (n) :
        for y in range (n) :
            if x != y :
                mat[x][y] +=1
    return mat


def verification_matrice (matrice, vecteur) :
    nn = len (vecteur)
    for i in range (nn) :
        if matrice[i][i] != 0 :
            xx = raw_input ('HOUSTON, pas nulle')
        for j in range (i+1, nn) :
            if matrice[vecteur[i]][vecteur[j-1]] > matrice[vecteur[i]] [vecteur[j]] :
                xx = raw_input ('HOUSTON   pas croissant')
            if matrice[i][j] != matrice[j][i] :
                xx = raw_input ('HOUSTON, pas symmetrique')


def construction_matrice_de_Robinson (n, jacta_est) :
    vecteur = list (range (n))
    random.shuffle (vecteur)
    #print '\nNouvel essai\n', vecteur ###########################################################
    matrice = matrice_vide (n)
    remplissage_Robinson (matrice, vecteur, jacta_est)
    #print 'fin construction de la matrice'
    verification_matrice (matrice, vecteur)
    return matrice



def ligne (val, longueur) :
    resul = list (range (longueur))
    for i in range (longueur) :
        resul [i] = val
    return resul


def construction_matrice_vertex_clique (l, D) :
    n = len (D)
    voisins = []
    for x in range (n) :
        voisins.append (construction_des_voisins (x, l, D))
    matrice = []
    for i in range (n*(l+1)) :
        matrice.append (ligne (0, n))
    for x in range (n) :
        for k in range (l+1) :
            for y in voisins[x][k] :
                matrice[(k * n) + x][y] = 1
    return matrice


def exemple_du_papier () :
    mat = [[0,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22],
           [0, 0, 9, 2,11, 6,11, 6, 6, 9,11, 6,11, 6, 5,11,11, 9,11, 6],
           [0, 0, 0, 9,11, 2,11, 3, 6, 1,11, 6,11, 6, 9,11,11, 1,11, 3],
           [0, 0, 0, 0,11, 6,11, 6, 6, 9,11, 6,11, 6, 1,11,11, 9,11, 6],
           [0, 0, 0, 0, 0,11, 8,11,11,11, 8,11, 8,11,11, 1, 8,11, 2,11],
           [0, 0, 0, 0, 0, 0,11, 3, 4, 2,11, 4,11, 4, 6,11,11, 2,11, 1],
           [0, 0, 0, 0, 0, 0, 0,11,11,11, 1,11, 5,11,11, 6, 3,11, 6,11],
           [0, 0, 0, 0, 0, 0, 0, 0, 4, 3,11, 4,11, 4, 6,11,11, 3,11, 2],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 5,11, 1,11, 3, 4,11,11, 5,11, 4],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 5,11, 6, 9,11,11, 1,11, 3],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 5,11,11, 7, 2,11, 6,11],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 2, 4,11,11, 5,11, 4],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11,11, 2, 5,11, 1,11],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,11,11, 6,11, 4],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11,11, 9,11, 6],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,11, 1,11],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 7,11],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11, 3],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,11],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    return complementation (mat)

def complementation (mat) :
    n = len (mat)
    for x in range (n) :
        for y in range (n) :
            if mat[x][y] == 0 :
                mat[x][y] = mat[y][x]
    return mat


def quasi_exemple_du_papier () :
    mat = exemple_du_papier ()
    for ligne in mat :
        ligne.append (22)
    n = len (mat)
    mat.append ([22] * n)
    mat[-1].append (0)
    return mat

def autre_exemple () :
    return [[0, 2.0, 3.0, 2.0, 0, 3.0, 2.0, 0, 1.0, 3.0],
[2.0, 0, 4.0, 4.0, 1.0, 4.0, 3.0, 1.0, 2.0, 4.0],
[3.0, 4.0, 0, 1.0, 3.0, 1.0, 1.0, 3.0, 1.0, 1.0],
[2.0, 4.0, 1.0, 0, 3.0, 1.0, 0, 3.0, 0, 1.0],
[0, 1.0, 3.0, 3.0, 0, 3.0, 3.0, 0, 2.0, 3.0],
[3.0, 4.0, 1.0, 1.0, 3.0, 0, 1.0, 3.0, 1.0, 0.0],
[2.0, 3.0, 1.0, 0, 3.0, 1.0, 0, 3.0, 0, 1.0],
[0, 1.0, 3.0, 3.0, 0, 3.0, 3.0, 0, 2.0, 3.0],
[1.0, 2.0, 1.0, 0, 2.0, 1.0, 0, 2.0, 0, 2.0],
[3.0, 4.0, 1.0, 1.0, 3.0, 0.0, 1.0, 3.0, 2.0, 0]]

def autre_exemple_2 () :
    return [[0, 415, 183, 38, 498, 517],
            [415, 0, 98, 309, 122, 211],
            [183, 98, 0, 109, 282, 360],
            [38, 309, 109, 0, 325, 412],
            [498, 122, 282, 325, 0, 4],
            [517, 211, 360, 412, 4, 0]]

def autre_exemple_3 () :
    return[[0, 558, 1, 362, 240, 589, 103, 641],
           [558, 0, 746, 72, 266, 95, 336, 193],
           [1, 746, 0, 407, 341, 921, 144, 1115],
           [362, 72, 407, 0, 112, 270, 157, 398],
           [240, 266, 341, 112, 0, 323, 100, 590],
           [589, 95, 921, 270, 323, 0, 342, 27],
           [103, 336, 144, 157, 100, 342, 0, 629],
           [641, 193, 1115, 398, 590, 27, 629, 0]]


def autre_exemple_4 () :
    return [[0, 3, 25, 1, 22, 3, 12, 15, 9, 16, 15, 19, 0],
            [3, 0, 30, 0, 27, 4, 15, 18, 12, 22, 18, 24, 4],
            [25, 30, 0, 27, 3, 19, 16, 8, 18, 7, 14, 6, 19],
            [1, 0, 27, 0, 23, 3, 15, 17, 12, 19, 15, 19, 1],
            [22, 27, 3, 23, 0, 14, 11, 8, 14, 4, 11, 1, 17],
            [3, 4, 19, 3, 14, 0, 2, 4, 0, 8, 4, 14, 3],
            [12, 15, 16, 15, 11, 2, 0, 4, 0, 7, 1, 10, 9],
            [15, 18, 8, 17, 8, 4, 4, 0, 4, 3, 2, 6, 13],
            [9, 12, 18, 12, 14, 0, 0, 4, 0, 8, 2, 13, 6],
            [16, 22, 7, 19, 4, 8, 7, 3, 8, 0, 4, 1, 14],
            [15, 18, 14, 15, 11, 4, 1, 2, 2, 4, 0, 9, 12],
            [19, 24, 6, 19, 1, 14, 10, 6, 13, 1, 9, 0, 16],
            [0, 4, 19, 1, 17, 3, 9, 13, 6, 14, 12, 16, 0]]


def autre_exemple_5 () :
    return [[0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
            [1, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0, 2, 0],
            [1, 1, 2, 0, 3, 3, 1, 1, 0, 3, 2, 0, 3],
            [1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 3, 0],
            [1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 3, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
            [1, 1, 2, 0, 2, 2, 1, 1, 0, 2, 2, 0, 2],
            [1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 3, 0],
            [1, 0, 0, 2, 0, 0, 0, 1, 2, 0, 0, 2, 0],
            [1, 1, 2, 0, 3, 3, 1, 1, 0, 3, 2, 0, 3],
            [1, 0, 0, 3, 0, 0, 0, 1, 2, 0, 0, 3, 0]]


def brouillage (matrice, k) :
    n = len (matrice)
    for i in range (n) :
        for j in range (i + 1, n) :
            matrice[i][j] += random.randint(0, k)
            matrice[j][i] = matrice[i][j]


def matrice_nulle (taille) :
    ligne = [0] * taille
    mat = []
    for i in range(taille) :
        la_ligne = list (ligne)
        mat.append(la_ligne)
    return mat


def test_brouillage () :
    matrice = exemple_du_papier()
    print( '\n\ndepart\n')
    for ligne in matrice :
        print (ligne)
    brouillage (matrice, 1)
    print ('\n\narrivee\n')
    for ligne in matrice :
        print (ligne)


def donnees_vartan () :
    mat = [[0,     1,     5,     5,     6,     7,    10,     6,     7,     7],
    [0,     0,     4,     6,     5,     8,    11,     7,     8,     8],
    [0,     0,     0,     6,     9,     8,     9,     7,     8,     8],
    [0,     0,     0,     0,     7,     6,     9,     5,     8,     8],
    [0,     0,     0,     0,     0,     5,    12,    10,    11,    11],
    [0,     0,     0,     0,     0,     0,     9,     9,     8,     8],
    [0,     0,     0,     0,     0,     0,     0,     4,     5,     9],
    [0,     0,     0,     0,     0,     0,     0,     0,     5,     7],
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     4],
    [0,     0,     0,     0,     0,     0,     0,     0,     0,     0]]
    return complementation(mat)

#test_brouillage()


## FIN CONSTRUCTION DISTANCE

