from tkinter import PhotoImage
from backwork.contact import*
class Evenement:
    def __init__(self,createur, image, toile):
        self.image = PhotoImage(file=image)
        self.toile = toile
        self.createur = createur
        self.attente = True
        self.link = None
        self.unended = True
        self.box = ['rect',self.toile.x_cam-125, self.toile.y_cam-75,self.toile.x_cam-25,self.toile.y_cam-25]
        self.time = 0
    
    def cond(self):
        return self.link!=None
    
    def clicked(self):
        _no = self.link
        self.toile.x = _no.x-self.toile.x_cam/2
        self.toile.y = _no.y-self.toile.y_cam/2
        self.createur.marque[0] = _no
    def tour(self, pas):
        if self.attente:
            if self.cond():
                self.apparence = self.toile.cnv.create_image(self.toile.x_cam-75,self.toile.y_cam-50, image=self.image)
                self.attente = False
        elif self.unended:
            self.time+=pas
            if self.toile.stats:
                if hitbox(self.box, ['point', self.toile.souris.x_cam, self.toile.souris.y_cam]):
                    self.clicked()
                    self.toile.stats = False
                    self.unended=False
                    self.toile.cnv.delete(self.apparence)
            if self.time>100:
                self.unended=False
                self.toile.cnv.delete(self.apparence)