from vivants.faune import*
from vivants.flore import*
from vivants.genes import apparente, ordre, aleatoires
from vivants.events import Evenement
from keyboard import is_pressed
from backwork.quad import*
class Divin:
    def __init__(self, toile, nb_protozoides=1, nb_plantes=1, nb_max = None, echantillon=200):
        self.cout_poid=[0.1,0.1,0.1,0,0.02,0.1,0.1, 0.1]+[0 for _ in range(13)]+[0.001, 0]
        self.cout_en = [0.02,0.01,0.01,0.001,0.001,0.001,0.001, 0.005]+[0 for _ in range(13)]+[0.01, 0]
        self.toile=toile
        self.evenements = [Evenement(self,'image/releve.png', self.toile)]
        self.actif = False
        if nb_max==None:
            self.pop_max = (nb_protozoides+nb_plantes)*2
        else:
            self.pop_max = nb_max
        self.quad = Quad(None, 0, 0, 0, toile.x_terrain, toile.y_terrain)
        self.population = [Animoide(self, toile, self.quad, toile.x_terrain, toile.y_terrain, nom='protozoide_n°'+str(i), gene=aleatoires()) for i in range(nb_protozoides)]+[Plantoide(self, toile, self.quad, toile.x_terrain, toile.y_terrain)for i in range(nb_plantes)]
        self.nb_animaux = nb_protozoides
        self.nb_bebe = 0
        self.max_gosses = 4
        self.incubateur = []
        self.statistiques = []
        self.echantillon = echantillon
        self.marque = [None, self.toile.cnv.create_oval(0,-1,0,-1, width=2, outline='red'), self.toile.cnv.create_oval(0,-1,0,-1, width=2, outline='green'), self.toile.cnv.create_oval(0,-1,0,-1, width=2, outline='blue')]
        self.x = self.toile.x_terrain/2
        self.y = self.toile.y_terrain/2
        self.calories = 100
    
    def tour(self, pas):
        for i in self.evenements:
            i.tour(pas)
        remplissage = self.calories/100
        if self.calories<100:
            self.calories += pas*2
        if remplissage>1:
            remplissage=1
            self.toile.centre_taille=12
            self.toile.centre_color='grey5'
        elif remplissage<0:
            replissage=0
            self.toile.centre_taille=4
            self.toile.centre_color='white'
        else:
            self.toile.centre_taille=(remplissage*8+4)
            self.toile.centre_color='grey15'
        for i in self.population:
            self.quad.insert(i)
        for i in self.population:
            i.tour(pas)
        self.affiche_stats()
        """proche = self.quad.proxi(self, self.toile.centre_r)
        for i in proche:
            if i.reigne=='A' and i.actif:
                i.orga[1].mange(self, pas*remplissage)"""
        self.naissances(pas)
        if self.nb_animaux==0:
            print('==========/!\exinction/!\=========')
            self.toile.end()
        else:
            if len(self.population)>self.pop_max:
                self.max_gosses=0
            else:
                self.max_gosses = int(((self.pop_max/len(self.population))**2)*2)
        self.quad.refresh()
    
    def materne(self, animoide1, animoide2):
        libre = True
        oeuf = None
        dist = disrap(animoide1.x, animoide2.x, animoide1.y, animoide2.y)
        for i in self.incubateur:
            for j in [1,2]:
                if i[j]==animoide1:
                    libre = False
                if i[j]==animoide2:
                    libre = False
            if i[1]==animoide2 and i[2]==animoide1:
                oeuf = i
        if libre:
            self.incubateur.append([False, animoide1, animoide2,0])
        else:
            if oeuf!=None:
                oeuf[0]=True
    
    def naissances(self, pas):
        for j,i in enumerate(self.incubateur):
            if i[0]:                   
                if self.max_gosses!=0:
                    for _ in range(randint(1,self.max_gosses)):
                        bebe = Animoide(self, self.toile, self.quad, self.toile.x_terrain, self.toile.y_terrain,
                                        gene=apparente(i[1], i[2]), generation=int(i[1].generation+i[2].generation+2)/2, nom='releve_n°'+str(self.nb_bebe))
                        bebe.x = (i[1].x+i[2].x)/2
                        bebe.y = (i[1].y+i[2].y)/2
                        if self.evenements[0].link==None:
                            self.evenements[0].link = bebe
                        bebe.age = 1
                        bebe.maturite = 1
                        for k in bebe.orga:
                            k.actu(pas)
                        bebe.tour(0)
                        for k in [1,2]:
                            i[k].energie-=(bebe.poid+bebe.energie)*2
                            i[k].nb_enfant+=1
                            i[k].orga[2].souvenir.renote(gosse=4)
                        self.population.append(bebe)
                        self.nb_animaux+=1
                        self.nb_bebe+=1
                        self.statistiques.append([i[0] for i in bebe.orga[0].potentiel]+[i[0] for i in bebe.orga[1].potentiel]+[i[0] for i in bebe.orga[2].potentiel]+[i[0] for i in bebe.orga[3].potentiel]+[bebe.generation])
                        if len(self.statistiques)>self.echantillon:
                            del(self.statistiques[0])
                del(self.incubateur[j])
            else:
                if i[3]>10:
                    del(self.incubateur[j])
                i[3]+=pas
    
    def mort(self, animoide):
        for i,j in enumerate(self.population):
            if j==animoide:
                if self.population[i].reigne=='A':
                        self.nb_animaux-=1
                del(self.population[i])

    
    def affiche_stats(self):
        if self.toile.stats:
            dist=10
            box=['circle', self.toile.souris.x, self.toile.souris.y, dist]
            items=self.quad.proxi(self.toile.souris, dist)
            if items!=[]:
                self.marque[0] = items[0]
            self.toile.stats = False
        if self.marque[0]!=None:
            self.toile.date.place(x=10, y=10)
            self.toile.age.set(self.stats(self.marque[0]))
            
            if self.marque[0].reigne =='A':
                v = self.marque[0].orga[3]
                r = v.vue
                x = v.etre.x + + avix(r*0.4, v.etre.d)
                y = v.etre.y + + aviy(r*0.4, v.etre.d)
                self.toile.coords(self.marque[3],x+r, y+r, x-r, y-r)
            else:
                self.toile.cnv.coords(self.marque[3],-1,-1,-1,-1)
            r= int(self.marque[0].taille*8)+3
            self.toile.coords(self.marque[1],self.marque[0].x+r, self.marque[0].y+r, self.marque[0].x-r, self.marque[0].y-r)
            if self.marque[0].cible[0]!=None:
                r= int(self.marque[0].cible[0].place)+3
                self.toile.coords(self.marque[2],self.marque[0].cible[0].x+r, self.marque[0].cible[0].y+r, self.marque[0].cible[0].x-r, self.marque[0].cible[0].y-r)
            else:
                self.toile.cnv.coords(self.marque[2], -1, -1, -1, -1)
            if is_pressed('p'):
                self.marque[0]=None
        else:
            for i in [1,2,3]:
                self.toile.cnv.coords(self.marque[i],-1,-1,-1,-1)
            
    def resultat(self):
        if len(self.statistiques)>0:
            ret = [0 for _ in self.statistiques[0]]
            for i in self.statistiques:
                for j,k in enumerate(i):
                    ret[j]+=k
            poid = 0
            en = 0
            for i in range(len(ret)):
                ret[i]=int(100*ret[i]/len(self.statistiques))/100
                poid+=int(ret[i]*self.cout_poid[i]*100)/100
                en+=int(ret[i]*self.cout_en[i]*100)/100  
            input('-----------:resultats:------------')
            print('poid_a_maturite________:', poid)
            print('consomation_a_maturite_:', en)
            print('puissance_motrice______:', ret[0])
            print('croissance_____________:', ret[10])
            print('santee_________________:', ret[1])
            print('recuperation___________:', ret[2])
            print('vitesse_de_rotation____:', ret[3])
            print('esperance_de_vie_(min)_:', ret[4])
            print("reserve_d'energie______:", ret[5])
            print("capacite_de_l'estomac__:", ret[6])
            print('vitesse_du_repas_______:', ret[7])
            print('faim_(1-0.5**x)________:', ret[8])
            print('cerveau================v')
            print('faim___________________:', ret[9])
            print('prudent________________:', ret[12])
            print('colereux_______________:', ret[13])
            print('amical_________________:', ret[14])
            print('paresse________________:', ret[15])
            print('gosse__________________:', ret[16])
            print('percistance____________:', ret[18])
            print('exploration____________:', ret[19])
            print('precision______________:', ret[20])
            print('vue____________________:', ret[21])
            print(',,,,,,,generation,,,,,,:', ret[len(ret)-1])
            print("echantillon: les", len(self.statistiques),'derniers nees')
            input('--:quitter:--')
        else:
            input('--:pas_de_donnee:--')
    
    def stats(self, bebe):
        ret = bebe.nom
        unpressed=True
        unpressedv = True
        surligne = 12
        if bebe.reigne=='A':
            ret+='\n ,,,,,,generation,,,,,,\t: '+str(bebe.generation)
            ret+='\n=============: etat :============='
            ret+='\n vie___________(pv)\t: '+str(int(bebe.vie[0]*10)/10)+'/'+str(int(bebe.vie[1]*10)/10)
            ret+='\n energie_______(en)\t: '+str(int(bebe.energie*10)/10)+'/'+str(int(bebe.reserve*10)/10)
            ret+='\n estomac_______(ca)\t: '+str(int(bebe.orga[1].remplissage*10)/10)+'/'+str(int(bebe.orga[1].stats[0]*10)/10)
            ret+='\n age__________(min)\t: '+str(int(bebe.age)+int((bebe.age%1)*6)/10)+'/'+str(int(bebe.longevite))
            if is_pressed('c'):
                ret+='\n==========: caracteristiques :========'
                ret+='\n maturite                        -\t: '+str(int(bebe.maturite))+ '/'+str(int(bebe.croissance))
                ret+='\n poid                            -\t: '+str(int(bebe.poid*10)/10)
                ret+='\n consomation___(en/10s)\t: '+str(int(bebe.besoin*100)/10)
                ret+='\n vitesse________(pix/s)\t: '+str(int(bebe.v_max*10)/10)
                ret+='\n magnabilite_____(pi/s)\t: '+str(int(bebe.orga[0].potentiel[3][0]*10/6)/10)
                ret+='\n regen___________(pv/s)\t: '+str(int(bebe.vie[2]*10)/10)
                ret+='\n faim______________(ca)\t: '+str(int(bebe.orga[1].stats[0]*10*(1-(0.9**bebe.orga[1].potentiel[3][0])))/10)
                ret+='\n nb_enfants________(ca)\t: '+str(bebe.nb_enfant)
                surligne-=8
            else:
                ret+='\n=======: caracteristiques :"c":=======v'
                if is_pressed('x'):
                    unpressed=False
                    rel=[i[0] for i in bebe.orga[0].potentiel]+[i[0] for i in bebe.orga[1].potentiel]
                    poid = 0
                    en = 0
                    for i in range(len(rel)):
                        poid+=(rel[i]*self.cout_poid[i])//0.1
                        en+=(rel[i]*self.cout_en[i]*10)//0.1
                    poid = str(int(poid/10))+'.'+str(int(poid%10))
                    en = str(int(en/10))+'.'+str(int(en%10))
                    ret+='\n===========: genes  :=============='
                    ret+='\n poid_adulte                      -\t: '+poid
                    ret+='\n conso_adulte____(en/s)\t: '+en
                    ret+='\n puissance_motrice     \t: '+str(rel[0])
                    ret+='\n santee_adulte_____(pv)\t: '+str(rel[1])
                    ret+='\n regen_adulte__(pv/10s)\t: '+str(rel[2])
                    ret+='\n magnabilite____(pi/6s)\t: '+str(rel[3])
                    ret+='\n longevite________(min)\t: '+str(rel[4])
                    ret+="\n reserve_energie__(5en)\t: "+str(rel[5])
                    ret+="\n capacite_estomac_(ca)\t: "+str(rel[6])
                    ret+="\n vitesse_de_repas(ca/5s)\t: "+str(rel[7])
                    ret+="\n faim________(1-0.5**x)\t: "+str(rel[8])
                    surligne-=11
            if unpressed:
                ret+='\n===========: genes  :"x":==========v'
                if is_pressed('b'):
                    ret+='\n deplacement \t: '
                    ret+=str(bebe.deplacement).split(' ')[2][12:]
                    ret+='\n action_____ \t: '
                    ret+=str(bebe.action).split(' ')[2][12:]
                    ret+='\n demarche___ \t: '
                    ret+=str(bebe.avancer).split(' ')[2][12:]
                    ret+='\n actif______ \t: '+str(bebe.actif)
                    surligne-=4
                elif is_pressed('v'):
                    unpressedv = False
                    vue = ''
                    ret+='\n ============: voit :============'
                    unseul = True
                    if bebe.cible[0]==None or bebe.orga[2].cible_consept==None:
                        ret+='\n ; None'
                    else:
                        ret+='\n ; '+bebe.cible[0].nom + ' ; ' +bebe.orga[2].cible_consept.nom + ' : '+str(int(bebe.cible[1]))
                    ret+='\n ; '+str(bebe.id_vue)
                    surligne-=2
                    for i in bebe.orga[2].consept:
                        if surligne>1:
                            ret += '\n '+i.nom+': '+str(i.element)+' '+str(i.nombre)
                            surligne-=1
                        elif surligne==1:
                            ret+= '\n ...'
                            surligne=0
                        elif unseul:
                            ret+='..'
                            unseul = False
                            surligne=0
                    for j, i in enumerate(bebe.orga[3].proximite):
                        if surligne>1:
                            ret += '\n '+i.nom+' => '+bebe.orga[2].tampon[j].nom
                            surligne-=1
                        elif surligne==1:
                            ret+= '\n ...'
                            surligne=0
                        elif unseul:
                            ret+='..'
                            unseul = False
                            surligne=0
            if unpressedv:
                ret+='\n ==========: voit :"v":=======v'
            for _ in range(surligne):
                ret+='\n    ||'
        else:
            ret+='\n calories   \t:'+str(int(bebe.calories*10)/10)
            ret+='\n age_(min)  \t:'+str(int(bebe.age)+int((bebe.age*6)%6)/10)+'/15'
        return(ret)
        