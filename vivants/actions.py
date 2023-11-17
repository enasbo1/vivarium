from backwork.direction import *

class Competences:
    #anim
    def affiche(self):
        if self.visible:
            dicorp = self.taille*5
            X=int(self.x+avix(dicorp, self.d))
            Y=int(self.y+aviy(dicorp, self.d))
            if not self.actif:
                X=int(self.x+avix(2, self.d))
                Y=int(self.y+aviy(2, self.d))
            if self.orga[1].remplissage<=0:
                if self.energie<self.reserve/3:
                    self.toile.cnv.itemconfig(self.tete, fill = 'red')
                else:
                    self.toile.cnv.itemconfig(self.tete, fill = 'purple')
            else:
                if self.energie<self.reserve/3:
                    self.toile.cnv.itemconfig(self.tete, fill = 'blue4')
                else:
                    self.toile.cnv.itemconfig(self.tete, fill = 'black')
            ditete = int(self.taille*3)
            dicorp = int(dicorp)
            pv=self.place*self.vie[0]/self.vie[1]
            manquant=self.place-pv
            if manquant>0.2:
                self.toile.cnv.itemconfig(self.corp, outline='red4', width=int((manquant)))
                dicorp=int((self.place-(manquant/2)+1))
            else:
                self.toile.cnv.itemconfig(self.corp, outline='black', width=1)
            self.d = lim(0,self.ecr_x,0,self.ecr_y, self.x, self.y, self.d)
            self.x, self.y = limxy(self.x, self.y, 0 ,self.ecr_x, 0, self.ecr_y)
            self.toile.coords(self.corp, int(self.x)+dicorp, int(self.y)+dicorp, int(self.x)-dicorp, int(self.y)-dicorp)
            self.toile.coords(self.tete, int(X)+ditete, int(Y)+ditete, int(X)-ditete, int(Y)-ditete)

    
    def boid(self, arg, pas):
        plproche, dist, direc = arg
        if plproche!=None:
            if dist<5:
                e = -1
                di=direc
            else:
                if dist>10:
                    e = 0.2
                    di = direc
                elif plproche.reigne=='A':
                    e = 0.5
                    di = plproche.d
                else:
                    e = 0
                    di = 0      
            self.d = tourne(self.d, di, pas*self.bracage*e*pi/10)
        self.avancer(pas)
        
    def fuir(self, arg, pas):
        plproche, dist, direc = arg
        if plproche!=None:
            e = -1
            di=direc
            self.d = tourne(self.d, di, pas*self.bracage*e*pi/10)
        self.avancer(pas)
    
    def tout_droit(self, arg, pas):
        self.cible = self.proche
        if self.proche[0]!=None:
            self.boid(self.proche, pas)
        else:
            self.avancer(pas)
        
    def rien(self, arg, pas):
        pass
    
    # vitesse de deplacement
    def arret(self, pas):
        pass
    
    def marcher(self, pas):
        if self.actif:
            self.x+=avix(self.v_max*pas, self.d)
            self.y+=aviy(self.v_max*pas, self.d)
            self.energie-=self.orga[0].stats[0]*pas/10
    
    def courir(self, pas):
        if self.actif:
            self.x+=avix(self.v_max*pas*2, self.d)
            self.y+=aviy(self.v_max*pas*2, self.d)
            self.energie-=self.orga[0].stats[0]*pas/3
    
    def approcher(self, arg, pas):
        plproche, dist, direc = arg
        if plproche!=None:
            e = 1
            di = direc
            self.d = tourne(self.d, di, pas*self.bracage*e*pi/10)
            if dist>2 and abs(rot(-self.d, direc))<pi/3:
                self.avancer(pas)
        else:
            self.avancer(pas)
    
    def reproduire(self, arg, pas):
        plproche, dist, direc = arg
        self.agit=False
        self.actif=True
        if plproche!=None:
            if self.maturite>10 and dist<10:
                self.act='!Rep'
                if plproche.reigne==self.reigne:
                    self.createur.materne(self, plproche)
                    self.agit = True
                    self.anim-= 2
                    plproche.aguicher(self)
                self.abandon()
        else:
            self.abandon()
    
    def manger(self, arg, pas):
        plproche, dist, direc = arg
        self.act='!Mng'
        self.agit=False
        self.actif=True
        if plproche!=None:
            if dist<5:
                self.orga[1].mange(plproche, self.anim)
                self.anim = 0
    
    def act_rien(self, arg, pas):
        self.agit = False
    
    def dormir(self, arg, pas):
        self.agit = False
        self.actif = False
        reveil = True
        if self.orga[1].vide:
            if self.energie<self.reserve/3:
                self.energie+=self.besoin*pas*2*self.vie[1]
                self.vie[0]-=self.besoin*pas*0.6*self.vie[1]
                reveil = False
        else:
            if self.energie<self.reserve and self.orga[1].rassasied:
                reveil = False
        if reveil:
            self.abandon()
    
    def abandon(self):
        self.alerte = True
        self.orga[2].choix = '!At'
    
    def aguicher(self, etre):
        self.abandon()
        self.orga[2].choix = '3'