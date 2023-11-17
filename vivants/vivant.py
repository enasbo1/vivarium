# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:10:25 2022

@author: idugardin
"""
from backwork.fonctions import base_4
from random import randint
from backwork.direction import*

class Etroide:
    def __init__(self, createur, toile, quad, x, y, nom='plante'):
        self.nom = nom
        self.ecr_x = x
        self.ecr_y = y
        self.id_vue = [0,"n0000","h0000","h0000"]
        self.poid = 0
        self.besoin = 0
        self.act = '!boid'
        self.reigne = 'P'
        self.visible = True
        self.createur = createur
        self.v_max=0
        self.calories=1
        self.taille = 0
        self.energie = 1000
        self.vie=[1,1,0.1]
        self.x=randint(200,x-200)
        self.y=randint(200,y-200)
        self.cible=(None, None, None)
        self.proche=(None, None, None)
        self.actif = False
        self.longevite = 15
        self.age = 1
        self.maturite=1
        self.croissance = self.longevite
        self.place = self.taille
        self.toile = toile
        self.corp = toile.cnv.create_oval(int(self.x)+5, int(self.y)+5, int(self.x)-5, int(self.y)-5, fill='green')
        self.quad=quad
        self.cont=quad
    
    def reinit(self):
        self.poid = 1
        self.calories = 1
        self.taille = 1
        if randint(0,2)==1:
            d = randint(-100,100)*pi/100
        else:
            d = randint(-5,5)*pi/5
        dist = self.toile.x_terrain
        if dist<self.toile.y_terrain:
            dist = self.toile.y_terrain
        dist = (dist/2)-200
        distance = randint(50,dist)
        self.x = (self.toile.x_terrain/2)-avix(distance, d)+randint(-100,100)+randint(-100,100)
        self.y = (self.toile.y_terrain/2)-aviy(distance, d)+randint(-100,100)+randint(-100,100)
        self.actif = False
        self.age = randint(0,100)/100
    
    def tour(self, pas):
        self.age += pas/60
        self.taille = self.poid**(1/3)
        self.id_vue[1] = 'n'+base_4(int(self.place))
        self.place = self.taille*5

