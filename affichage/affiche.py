from tkinter import*
from affichage.souris import Souris
from keyboard import is_pressed
class Toile:
    def __init__(self, x_cam, y_cam, x_terrain, y_terrain, title='unknow', fond = "pale turquoise", vitesse_lente = 5, vitesse_rapide=100):
        self.x_cam = x_cam
        self.y_cam = y_cam
        self.acceleration = 1
        self.x_terrain = x_terrain
        self.y_terrain = y_terrain
        self.horloge = 0
        self.a_jours=0
        self.cont = True
        self.vitesse = vitesse_lente
        self.allure = [vitesse_lente, vitesse_rapide]
        self.boite = [True,0]
        self.visible = [True, True]
        self.annee = ''
        self.texte = ''
        self.stats = False
        self.souris = Souris()
        self.fenetre=Tk()
        self.centre_r = int((self.x_terrain+self.y_terrain)/20)
        self.fenetre.attributes('-fullscreen', True)
        self.fenetre.bind('<Escape>',lambda e: self.end())
        self.fenetre.title(title)
        self.fenetre.geometry(str(x_cam+10)+'x'+str(y_cam+10))
        self.cnv = Canvas(self.fenetre, width = x_cam, height = y_cam, bg=fond)
        self.cnv.place(x=5,y=5)
        self.cnv.bind('<Button-1>', self.onclick)
        self.age = StringVar()
        self.age.set(self.annee)
        self.voile = Canvas(self.fenetre, width = x_cam, height = y_cam, bg='black')
        self.voile.place(x=0, y=-self.y_cam-5)
        self.date = Label(self.fenetre, textvariable = self.age ,fg = 'white',bg = 'blue', font=18, width = 34, height = 25, justify='left')
        self.date.place(x=0, y=-40)
        self.x = (x_terrain-x_cam)/2
        self.y = (y_terrain-y_cam)/2
        self.vue_d_ensemble = False
        self.centre_color = "grey"
        self.centre_taille = 12
        self.ile = self.cnv.create_rectangle(0,0,0,0,fill='DarkOliveGreen1')
        self.sommet = self.cnv.create_oval(0,0,0,0, fill='PaleGreen1', width=self.centre_taille, outline=self.centre_color)
    
    def coords(self, item, x1, y1, x2, y2):
        if self.visible[0]:
            if self.vue_d_ensemble:
                X=2
                Y=2
                echelle = (self.x_cam-4)/self.x_terrain
                if echelle>(self.y_cam-4)/self.y_terrain:
                    echelle=(self.y_cam-4)/self.y_terrain
                    X+=(self.x_cam-(self.x_terrain*echelle))/2
                else:
                    Y+=(self.y_cam-(self.y_terrain*echelle))/2
                self.cnv.coords(item, int(x1*echelle)+X, int(y1*echelle)+Y, int(x2*echelle)+X, int(y2*echelle)+Y)
            else:
                self.cnv.coords(item, x1-self.x, y1-self.y, x2-self.x, y2-self.y)
    
    def moove(self, temps):
        self.annee = str(int(self.horloge)+(int((self.horloge%1)*6)/10))
        self.age.set(self.texte)
        if self.visible[0]:
            self.date.place(x=-1000, y=-1000)
            touche = False
            self.vue_d_ensemble = False
            if is_pressed('z'):
                self.y-=temps*100*self.acceleration
                touche = True
            if is_pressed('s'):
                self.y+=temps*100*self.acceleration
                touche = True
            if is_pressed('d'):
                self.x+=temps*100*self.acceleration
                touche = True
            if is_pressed('q'):
                self.x-=temps*100*self.acceleration
                touche = True
            if is_pressed(' '):
                self.vue_d_ensemble = True
                self.x = (self.x_terrain-self.x_cam)/2
                self.y = (self.y_terrain-self.y_cam)/2
            if is_pressed('e'):
                if self.boite[0]:
                    self.boite[1]=(self.boite[1]+1)%2
                    self.boite[0]=False
            else:
                self.boite[0]=True
            if touche:
                if self.acceleration<10:
                    self.acceleration+=temps*5
                else:
                    self.acceleration=10
            else:
                self.acceleration = 1
            self.cnv.itemconfig(self.sommet, outline=self.centre_color, width=self.centre_taille)
            self.coords(self.sommet, (self.x_terrain/2)-self.centre_r,(self.y_terrain/2)-self.centre_r,(self.x_terrain/2)+self.centre_r, (self.y_terrain/2)+self.centre_r)
            self.coords(self.ile, 0,0,self.x_terrain, self.y_terrain)
        else:
            self.a_jours-=temps
            self.boite[1]=1
        if is_pressed('a'):
            if self.visible[1]:
                if self.visible[0]:
                    self.voile.place(x=5, y=5)
                    self.date.place(x=int(self.x_cam/2)-297, y=int(self.y_cam/2)-180)
                    self.cnv.update()
                else:
                    self.voile.place(x=0, y=-self.y_cam-5)
                self.visible[0]=not self.visible[0]
                self.a_jours=0
                self.visible[1]=False
        else:
            self.visible[1]=True
        self.vitesse=self.allure[self.boite[1]]
    
    def update(self):
        if self.visible[0]:
            self.cnv.update()
        else:
            if self.a_jours<0:
                self.date.update()
                self.a_jours+=1

    def onclick(self, event):
        if not self.vue_d_ensemble:
            self.souris.x = event.x+self.x
            self.souris.y = event.y+self.y
            self.souris.x_cam = event.x
            self.souris.y_cam = event.y
            self.stats = True
        
    
    def end(self):
        self.cont=False
        self.cnv.update()