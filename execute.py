from backwork.noeud import*
from time import*
from affichage.affiche import*

x_terrain=7000
y_terrain=7000
x_cam = 1522
y_cam = 850

toile=Toile(x_cam, y_cam, x_terrain, y_terrain, title="vivarium", vitesse_lente=2.5)
createur = Divin(toile, nb_protozoides=300, nb_plantes=800, nb_max = 1300)

bande=toile.cnv.create_text(x_cam/2, 20, text='0')

toile.update()
t=time()
sleep(0.1)
fps = [1,0]
while toile.cont:
    T=time()
    if T-t>0.5/toile.vitesse:
        temps = (T-t)
        pas = 0.5
        if toile.visible[0]:
            toile.texte = toile.annee+' ; ['+str(int(5*fps[0])/10)+'] ; '+str(createur.nb_animaux)
        else:
            toile.texte = toile.annee+' ; ['+str(int(0.5*fps[0]/60)+(int((fps[0]*0.5)%60)/100))+'] ; '+str(createur.nb_animaux)
    else:
        temps = (T-t)
        pas = (T-t)*toile.vitesse
        if pas>0:
            toile.texte = toile.annee+' ; '+str(fps[0])+' ; '+str(createur.nb_animaux)
        else:
            toile.texte = toile.annee+'; +++ ; '+str(createur.nb_animaux)
    toile.cnv.itemconfig(bande, text=toile.texte)
    fps[1]-=temps
    if fps[1]<=0:
        fps[0]=int(10/temps)/10
        fps[1]+=0.4
    t=time()
    if temps>0.1:
        temps = 0.1
    toile.horloge+=pas/60
    toile.moove(temps)
    createur.tour(pas)
    toile.update()
toile.cnv.update()
toile.fenetre.destroy()
print(',,,,,,,annee,,,,,,,:',toile.annee)
createur.resultat()