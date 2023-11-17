from backwork.fonctions import correspondance

class Consept:
    def __init__(self, element, nom='none'):
        self.element=[i for i in element]
        self.nom = nom
        self.occur = 1
        self.peur  = 1
        self.amitie = 1
        self.amour = 0
        self.colere = 1
        self.mangeable = 1
        self.actu = None
        self.distance=0
        self.nombre = 0
    
    def rebout(self):
        self.actu = None
        self.distance=0
        self.nombre = 0

    def jour(self, etre):
        self.occur  = self.occur/(1+2**(-etre.memoire))
        self.amitie = self.amitie/(1+2**(-etre.memoire))
        self.amour  = self.amour/(1+2**(-etre.memoire))
        self.peur   = self.peur/(1+2**(-etre.memoire))
        self.colere = self.colere/(1+2**(-etre.memoire))
    
    def compare(self, info):
        rep = [0]
        for i in self.element:
            for j in info:
                if i[0]==j[0]:
                    a=correspondance(i,j)
                    if a>rep[i[0]]:
                        rep[i[0]]=a
        b=0
        for i in rep:
            b+=i
        return b
    
    def prems(self, cible, distance):
        self.actu = cible
        self.distance = distance
        self.nombre = 1
    
    def ajout(self, cible, distance2):
        if self.actu==None or distance2<self.distance:
            self.actu = cible
            self.distance = distance2
            self.nombre +=1
    
    def addit(self, souvenir):
        self.peur += souvenir.note_aie
        self.amitie += souvenir.note_affect
        self.amour += souvenir.note_gosse
        self.colere += souvenir.note_aie
        self.mangeable += souvenir.note_manger
    
    def donnee(self, souvenir):
        self.peur = souvenir.note_aie
        self.amitie = souvenir.note_affect
        self.amour = souvenir.note_gosse
        self.colere = souvenir.note_aie
        self.mangeable = souvenir.note_manger