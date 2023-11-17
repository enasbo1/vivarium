from IA.consepts import Consept
from backwork.direction import*

class Souvenirs:
    def __init__(self, proprio):
        self.proprio = proprio
        self.note_aie = 0
        self.note_gosse = 0
        self.note_manger = 0
        self.note_affect = 0
        self.note_colere = 0
        self.cible_consept = None
    
    def reset(self, cible_consept, cible_info, act, cible):
        self.__init__(self.proprio)
        self.cible_consept = cible_consept
        self.cible = cible
        self.cible_info = cible_info[:]
        self.act = act
    
    def renote(self, aie=0, gosse=0, manger=0, ami=0):
        self.note_affect += ami
        self.note_aie += aie
        self.note_gosse += gosse
        self.note_manger += manger
        self.note_colere += aie
    
    def tour(self):
        divergence = (self.note_aie-self.cible_consept.peur)**2+(self.note_gosse-self.cible_consept.amour)**2+(self.note_affect-self.cible_consept.amitie)**2+(self.note_manger-self.cible_consept.mageable)**2
        if divergence>self.proprio.precision**2:
            proprio = self.proprio
            distance = disrap(proprio.x, proprio.y, self.cible_info[0].x, self.cible_info[0].y)
            new = Consept(self.cible_info, distance)
            self.proprio.consept.append(new)
            new.donnee(self)
            self.proprio.alerte = True
    
    def actualise(self):
        divergence = ((self.note_aie-self.cible_consept.peur)**2+((self.note_gosse-self.cible_consept.amour)*self.proprio.etre.maturite>10)**2+(self.note_affect-self.cible_consept.amitie)**2+(self.note_manger-self.cible_consept.mangeable)**2)*(1-self.cible_consept.compare(self.cible_info))
        if divergence>(self.proprio.precision**2):
            consept = self.proprio.reconnaitre(self.cible)
            if consept==self.cible_consept:
                proprio = self.proprio.etre
                distance = disrap(proprio.x, proprio.y, self.cible.x, self.cible.y)
                new = Consept(self.cible_info, nom= 'n°'+str(len(self.proprio.consept)-1))
                self.proprio.consept.append(new)
                new.donnee(self)
            else:
                consept.addit(self)
        else:
            self.cible_consept.addit(self)