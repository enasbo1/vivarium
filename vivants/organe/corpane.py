from random import randint
from math import*
class Corp:
    def __init__(self, etre, gene):
        self.potentiel = gene[0]
        self.stats = [i[0]/20 for i in self.potentiel]
        self.etre = etre
        for i,j in enumerate(self.potentiel):
            self.etre.poid += j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
            
    def actu(self, pas):
        for i, j in enumerate(self.potentiel):
            self.stats[i]=j[0]*self.etre.maturite/20
        for i,j in enumerate(self.potentiel):
            self.etre.poid+=j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
        self.etre.v_max = self.stats[0]*5/self.etre.poid
        self.etre.vie[1] = self.stats[1]
        self.etre.vie[2] = self.stats[2]/10
        self.etre.bracage = self.potentiel[3][0]*pi/6
        self.etre.longevite = self.potentiel[4][0]
        self.etre.reserve = self.stats[5]*5