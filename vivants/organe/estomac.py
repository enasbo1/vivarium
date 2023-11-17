class Ventre:
    def __init__(self, etre, gene):
        self.potentiel = gene[1]
        self.stats = [i[0]/20 for i in self.potentiel]
        self.etre = etre
        self.remplissage = self.stats[0]*5
        for i,j in enumerate(self.potentiel):
            self.etre.poid += j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
    
    def actu(self, pas):
        for i, j in enumerate(self.potentiel):
            self.stats[i]=j[0]*self.etre.maturite/20
        for i,j in enumerate(self.potentiel):
            self.etre.poid+=j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
        self.etre.estomac=self
        self.etre.energie+=pas*0.1
        if self.remplissage > 0 and self.etre.energie<self.etre.reserve:
            if self.etre.actif:
                if self.remplissage<pas/20:
                    self.etre.energie+=self.remplissage/2
                    self.remplissage=0
                else:
                    self.remplissage-=pas/20
                    self.etre.energie+=pas/2
            else:
                if self.remplissage<pas*2:
                    self.etre.energie+=self.remplissage*2
                    self.remplissage=0
                else:
                    self.remplissage-=pas*2
                    self.etre.energie+=pas*20
        if self.etre.energie>=self.etre.reserve:
            self.remplissage-=pas/20
        if self.etre.energie>self.etre.reserve:
            self.etre.energie=self.etre.reserve
        self.plein = self.remplissage>=self.stats[0]
        self.etre.faim = self.remplissage<self.stats[0]
        self.rassasied = self.remplissage>(self.stats[0]*(1-(0.9**self.potentiel[3][0])))
        self.vide = self.remplissage<=0
    
    def envie(self):
        if self.plein:
            return 0
        elif self.remplissage>0:
            return self.stats[0]*self.potentiel[2][0]/self.remplissage
        else:
            return 'abs'
    
    def fatigue(self):
        if self.etre.energie<=0:
            return 'abs'
        elif self.etre.energie<2*self.etre.reserve/3 and self.plein:
            return 'abs'
        elif self.etre.energie>=self.etre.reserve:
            return 0
        elif self.plein:
            return 0
        else:
            return self.stats[0]*self.etre.orga[2].paresse*self.etre.reserve/((self.stats[0]-self.remplissage)*self.etre.energie)
    
    def mange(self, cible, pas):
        if cible.calories>0 and not self.plein and not cible.actif:
            cible.calories-=pas*self.stats[1]/5
            self.remplissage+=pas*self.stats[1]/5
            self.etre.orga[2].souvenir.renote(manger=pas*self.stats[1]/5)
        else:
            self.etre.abandon()
        