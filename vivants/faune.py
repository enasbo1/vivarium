from random import randint
from vivants.genes import protozoide
from backwork.direction import*
from vivants.organe.corpane import Corp
from vivants.organe.estomac import Ventre
from vivants.organe.cerveau import Cerveau, IA
from vivants.organe.yeux import Oeuil
from random import randint
from IA.consepts import Consept
from backwork.fonctions import*
from IA.souvenirs import Souvenirs
from vivants.actions import Competences
from vivants.vivant import Etroide

class Animoide(Etroide, Competences):
    def __init__(self, createur, toile, quad, x, y, gene=protozoide(), generation=0, nom=''):
        super().__init__(createur, toile, quad, x, y , nom=nom)
        self.generation = generation
        self.reigne = 'A'
        self.surnom = self.nom
        self.nb_enfant = 0
        self.id_vue = [0, "n1111", "h2222","h2222"]
        self.reserve=0.1
        self.orga = [Corp(self, gene), Ventre(self, gene), Cerveau(self, gene), Oeuil(self, gene)]
        self.d=randint(-10,12)*pi/10
        self.maturite=self.age
        distance = randint(0,toile.centre_r*3)
        self.x = (toile.x_terrain/2)-avix(distance, self.d)
        self.y = (toile.y_terrain/2)-aviy(distance, self.d)
        self.deplacement = self.boid
        self.action = self.reproduire
        self.avancer = self.marcher
        self.faim = True
        self.actif = True
        self.anim = 0
        self.alerte = True
        self.tete = toile.cnv.create_oval(0,0,0,0, fill='black')
        toile.cnv.itemconfig(self.corp, fill='blue')
        for i in self.orga:
            i.actu(0)
        self.age = randint(1, int(self.longevite))
        self.energie = self.reserve
        self.maturite = self.age
    
    def tour(self, pas):
        super().tour(pas)
        self.poid = 0
        self.besoin = 0
        viellesse = self.age-self.longevite
        if viellesse>0:
            self.vie[0]-=(viellesse**2)*pas*randint(0,6)/40
        for i in self.orga:
            i.actu(pas)
        if self.maturite<self.croissance:
            self.maturite+=pas/150
            if self.energie>(self.reserve/3):
                self.maturite+=pas/20
                self.energie-=self.besoin*pas
        else:
            self.maturite = self.croissance
        self.nom = self.surnom+' : '+self.orga[2].choix
        if self.vie[0]>0:
            if self.vie[0]<self.vie[1] and self.energie>self.reserve/3:
                self.vie[0]+=self.vie[2]*pas
                self.energie-=pas
            if self.vie[0]>=self.vie[1]:
                self.vie[0]=self.vie[1]
            plproche, dist, direc = self.cont.proche(self, self.orga[3].vue)
            if self.actif:
                self.energie-=self.besoin*pas
            self.anim+=pas
            if plproche!=None:
                dimin = self.place+plproche.place+1
                dist -= dimin
                self.proche =(plproche, dist, direc)
                if dist<=0:
                    if plproche.reigne=='A':
                        energie = (self.v_max*self.poid+plproche.v_max*plproche.poid)/2
                    else:
                        energie = (self.v_max*self.poid+plproche.v_max*plproche.poid)
                    self.x+=avix(-energie*pas/self.poid, direc)
                    self.y+=aviy(-energie*pas/self.poid, direc)
                    plproche.x-=avix(-energie*pas/plproche.poid, direc)
                    plproche.y-=aviy(-energie*pas/plproche.poid, direc)
            self.cible = self.orga[2].info()
            self.deplacement(self.cible, pas)
            self.agit = True
            while self.anim>0 and self.agit:
                self.action(self.cible, pas)
            if self.anim>0:
                self.anim=0
            self.affiche()
        else:
            self.kill()
    
    def kill(self):
        self.actif=False
        self.visible=False
        self.toile.cnv.delete(self.corp)
        self.toile.cnv.delete(self.tete)
        self.createur.mort(self)
        

