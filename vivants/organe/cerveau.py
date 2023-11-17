from IA.classi import *
from backwork.direction import*
class Cerveau(IA):
    def __init__(self, etre, gene): #gene2; taille 1 
        super().__init__()
        self.potentiel = gene[2]
        self.stats = [i[0]/20 for i in self.potentiel]
        self.etre = etre
        self.consept = [Consept([self.etre.id_vue], nom = 'simili'), Consept([[0,"n3100","h0000","h0000"]], nom = 'herbi'), Consept([[0,"n2000","h1111","h1111"]], nom = 'tronc'),Consept([[0,"n2000"]+[self.etre.id_vue[i] for i in range(2,4)]], nom = 'bebe')]
        self.consept[0].peur = 0
        self.consept[0].amitie = 1
        self.consept[0].colere = 0
        self.consept[0].amour = 3
        self.consept[0].mangeable = 0
        self.consept[1].peur = 0
        self.consept[1].amitie = 0
        self.consept[1].colere = 0
        self.consept[1].amour = 0
        self.consept[1].mangeable = 2
        self.consept[2].peur = 0
        self.consept[2].amitie = 0
        self.consept[2].colere = 0
        self.consept[2].amour = 0
        self.consept[2].mangeable = 0
        self.consept[3].peur = 0
        self.consept[3].amitie = 0
        self.consept[3].colere = 0
        self.consept[3].amour = 0
        self.consept[3].mangeable = 0
        self.tampon = []
        self.fini = False
        self.souvenir = Souvenirs(self)
        self.jour = 0
        self.choix = ''
        self.cible = None
        self.unfin = True
        self.base = {'!At':self.rien, '!M':self.marche, '!C': self.cours,
            '!N': self.repas, '!Gniap': self.mordre, '!D': self.dormir, 
            '!Rep': self.reproduire, '!Charge':self.charge, '!Fuit':self.fuite,
            '!Suis':self.suivre, '!Alerte': self.alerte}
        self.demarche = {'.Imite': self.imite}
        for i,j in enumerate(self.potentiel):
            self.etre.poid += j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
        
    def actu(self, pas):
        self.jour+=pas
        for i, j in enumerate(self.potentiel):
            self.stats[i]=j[0]*self.etre.maturite/20
        for i,j in enumerate(self.potentiel):
            self.etre.poid+=j[1]*self.stats[i]
            self.etre.besoin += j[2]*self.stats[i]
        self.instincs()
        self.etre.croissance = self.etre.longevite*(1-(0.9**self.potentiel[0][0]))
        self.memoire = self.stats[1]
        self.prudent = self.potentiel[2][0]
        self.colereux = self.potentiel[3][0]
        self.amical = self.potentiel[4][0]
        self.paresse = self.potentiel[5][0]
        self.gosse = self.potentiel[6][0]*(self.etre.maturite>10)
        self.percistance = 1+(self.potentiel[7][0]/10)
        self.initiative = 0 #self.potentiel[8][0]
        self.exploration = self.potentiel[9][0]
        self.precision = self.potentiel[10][0]
        self.surveillance()
        if self.cible!=None:
            if self.etre.orga[3].unvisible(self.cible):
                self.etre.alerte=True
        self.changer()
        if self.etre.alerte:
            self.etre.alerte=False
            if self.change:
                self.peciste()
                self.choisir()
        self.unfin = True
        while self.unfin:
            self.agir()
        if self.fini:
            if self.souvenir.cible_consept!=None:
                self.souvenir.actualise()
            if self.cible!=None and self.cible_consept!=None:
                self.souvenir.reset(self.cible_consept, [self.cible.id_vue], self.choix, self.cible)
        if self.jour>60:
            for i in self.consept:
                i.jour(self)
    
    def surveillance(self):
        if self.cible!=None:
            if self.etre.orga[3].unvisible(self.cible):
                self.etre.alerte=True
            if self.cible.vie[0]<=0:
                self.alerte = True
    
    def rien(self, args):
        self.unfin = False
    
    def marche(self, arg):
        self.etre.actif = True
        self.etre.avancer = self.etre.marcher
    
    def cours(self, arg):
        self.etre.actif = True
        self.etre.avancer = self.etre.courir
    
    def repas(self, arg):
        self.etre.actif = True
        self.etre.action = self.etre.manger
    
    def mordre(self, arg):
        pass
    
    def imite(self, arg):
        if self.cible.reigne=='A':
            self.etre.actif  = True
            if self.cible.orga[2].choix!='':
                self.act=self.cible.orga[2].choix
                self.choix = self.cible.orga[2].choix
            else:
                self.act ='!At .Imite'
        else:
            self.etre.abandon()
        
    def dormir(self, arg):
        self.etre.actif = False
        self.etre.avancer = self.etre.arret
        self.etre.action = self.etre.dormir
    
    def reproduire(self, arg):
        self.etre.actif = True
        self.etre.action = self.etre.reproduire
    
    def charge(self, arg):
        self.etre.deplacement=self.etre.approcher
    
    def fuite(self, arg):
        self.etre.deplacement = self.etre.fuir
    
    def suivre(self, arg):
        self.etre.deplacement = self.etre.boid
    
    def alerte(self, arg):
        self.etre.alerte = True
        self.etre.actif = True
        self.unfin = False
        self.etre.avancer = self.etre.marcher
        self.etre.deplacement = self.etre.tout_droit
        self.etre.action = self.etre.act_rien
    
    def info(self):
        if self.cible==None or self.cible_consept==None:
            return(None, None, None)
        else:
            return(self.cible, dis(self.etre.x,self.etre.y,self.cible.x,self.cible.y)-(self.etre.place+self.cible.place+1), dir(self.etre.x, self.etre.y,0, self.cible.x, self.cible.y))
    
    def agir(self):
        self.decode()
        self.action(self.arg)
        if self.act == '':
            self.unfin = False
            
    def conseptualiser(self, visible):
        for i in self.consept:
            i.rebout()
        self.tampon=[0 for _ in visible]
        for i,j in enumerate(visible):
            self.tampon[i] = self.reconnaitre(j)
    
    def reconnaitre(self, item):
        ident = [item.id_vue[:]]
        temp = -1
        diff = -1
        for m,n in enumerate(self.consept):
            if diff==-1:
                temp = n
                diff = n.compare(ident)
            else:
                k = n.compare(ident)
                if k>diff and k!=-1:
                    temp = n
                    diff = k
        if diff == -1:
            new = Consept(ident)
            new.prems(item, disrap(item.x, item.y, self.etre.x, self.etre.y))
            self.consept.append(new)
            return new
        else:
            temp.ajout(item, disrap(item.x, item.y, self.etre.x, self.etre.y))
            return temp

    
    def changer(self):
        self.sentiment()
        self.change = True
        if self.sommeil=='abs':
            self.act = '5'
            self.choix = '5 !At'
            self.change = False
            self.cible = None
            self.fini = True
        elif self.affame=='abs':
            self.change = False
            self.conseptualiser(self.etre.orga[3].sens())
            le = lambda x: x.mangeable
            choix = '4 !At'
            cible = None
            intence = 0
            for i in self.tampon:
                _temp = le(i)
                if intence < _temp:
                    intence = _temp
                    cible = i.actu
                    cible_consept = i
            if choix!=self.choix or cible!=self.cible:
                if cible!=None:
                    self.cible = cible
                    self.cible_consept = cible_consept
                    #self.cible.attaquants.append(self)
                    self.act = '4'
                    self.choix = '4 !At'
                else:
                    self.act='6'
                    self.choix = '6'
                    self.cible = None
                    self.cible_consept = None
                self.fini = True
    
    def choisir(self):
        self.conseptualiser(self.etre.orga[3].sens())
        peur = 0
        colere = 0
        amour = 0
        amitie = 0
        faim = 0
        sommeil = self.sommeil
        explore = self.exploration
        for i in self.tampon:
            peur += i.peur*self.peureux
            amitie += i.amitie*self.amical
            colere += i.colere*self.agressif
            amour += i.amour*self.amour
            faim += i.mangeable*self.affame
        le = lambda x : 0
        emo = sommeil
        choix = '5'
        if emo<explore:
            choix = '6'
            emo = explore
        if randint(1, int(self.initiative+10))>self.initiative:
            if emo<peur:
                le = lambda x : x.peur
                emo = peur
                choix = '0'
            if emo<amitie:
                emo = amitie
                le = lambda x : x.amitie
                choix = '1'
            if emo<colere:
                emo = colere
                le = lambda x : x.colere
                choix = '2'
            if emo<amour:
                le = lambda x : x.amour
                choix = '3'
            if emo<faim:
                le = lambda x : x.mangeable
                choix = '4'
        else:
            i=randint(0,4)
            le = lambda x : x.peur
            if i==1:
                le = lambda x : x.amitie
            if i==2:
                le = lambda x : x.colere
            if i==3:
                le = lambda x : x.amour
            if i==4:
                le = lambda x : x.mangeable
            choix = str(i)
        
        if choix=='5':
            self.cible = None
            self.act ='5'
            self.choix = '5'
            self.fini = True
        elif choix=='6':
            self.cible = None
            self.act ='6'
            self.choix = '6'
            self.fini = True
        else:
            cible = None
            intence = 0
            for i in self.tampon:
                _temp = le(i)
                if intence < _temp:
                    intence = _temp
                    cible = i.actu
                    cible_consept = i
            if choix!=self.choix or cible!=self.cible:
                if cible!=None:
                    self.cible = cible
                    self.cible_consept = cible_consept
                    #self.cible.attaquants.append(self)
                    self.act = choix
                    self.choix = choix
                else:
                    self.act='!Alerte'
                    self.cible_consept = None
                    self.cible = None
                self.fini = True

    def sentiment(self):
        self.peureux = (1-((self.etre.vie[0]/self.etre.vie[1])**2))*self.prudent
        self.agressif = self.colereux
        self.affame = self.etre.orga[1].envie()
        self.amour = self.gosse*(self.etre.maturite>10)
        self.sommeil = self.etre.orga[1].fatigue()
        self.amical1 = self.amical
    
    def peciste(self):
        if self.choix=='0':
            self.peureux=self.peureux*self.percistance
        if self.choix=='1':
            self.amical1=self.amour*self.percistance
        if self.choix=='2':
            self.agressif=self.agressif*self.percistance
        if self.choix=='3':
            self.amour=self.amour*self.percistance
        if self.choix=='4':
            self.affame=self.affame*self.percistance
        if self.choix=='5':
            self.sommeil=self.sommeil*self.percistance
    
    def instincs(self):
        self.consept[0].amour = 3
        self.consept[1].mangeable = 2

        
