# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 14:10:25 2022

@author: idugardin
"""

from random import randint
from vivants.vivant import Etroide
from backwork.direction import*

class Plantoide(Etroide):
    def __init__(self, createur, toile, quad, x, y):
        super().__init__(createur, toile, quad, x, y)
        self.age = randint(0,1000)/100
        self.poid = randint(0,1000)/100
        self.calories = self.age*3.3
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
        aug = pas*randint(1,6)/60
        if not self.actif:
            self.id_vue[2] = 'h0000'
            self.id_vue[3] = 'h0000'
            self.calories += aug
            self.poid = self.calories
            self.toile.cnv.itemconfig(self.corp, fill='green')
        else:
            self.toile.cnv.itemconfig(self.corp, fill='brown')
            self.id_vue[2] = 'h1111'
            self.id_vue[3] = 'h1111'
            self.calories = 0
            if self.age>=self.longevite*0.7:
                self.reinit()
        if self.poid<=0.4:
            self.poid=0.5
            self.actif = True
        super().tour(pas)
        self.place = self.taille*3
        if self.age>=self.longevite:
            self.reinit()
        dicorp = int(self.place)
        self.x, self.y = limxy(self.x, self.y, 0 ,self.ecr_x, 0, self.ecr_y)
        self.toile.coords(self.corp, int(self.x)+dicorp, int(self.y)+dicorp, int(self.x)-dicorp, int(self.y)-dicorp)
    
    def kill(self):
        self.actif=False
        self.visible=False
        self.toile.cnv.delete(self.corp)
        self.createur.mort(self)
