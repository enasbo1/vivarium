from backwork.direction import disrap,avix,aviy

class Oeuil:
    def __init__(self, etre, gene):
        self.potentiel = gene[3]
        self.stats = [i[0]/20 for i in self.potentiel]
        self.proximite = []
        self.etre = etre
        self.vue = 10
        for i,j in enumerate(self.potentiel):
            self.etre.poid += j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
            
    def actu(self, pas):
        for i, j in enumerate(self.potentiel):
            self.stats[i]=j[0]*self.etre.maturite/20
        for i,j in enumerate(self.potentiel):
            self.etre.poid+=j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
        self.vue = (self.etre.taille+self.stats[0]+2)*10
    
    def sens(self):
        x = self.etre.x
        y = self.etre.y
        self.etre.x = self.etre.x + avix(self.vue*0.4, self.etre.d)
        self.etre.y = self.etre.y + aviy(self.vue*0.4, self.etre.d)
        self.proximite = self.etre.quad.proxi(self.etre, self.vue)
        self.etre.x = x
        self.etre.y = y
        return self.proximite

    def unvisible(self, item):
        x = self.etre.x + avix(self.vue*0.4, self.etre.d)
        y = self.etre.y + aviy(self.vue*0.4, self.etre.d)
        return disrap(x, y, item.x, item.y)>self.vue**2