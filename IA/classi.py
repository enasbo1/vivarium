from random import randint
from IA.consepts import Consept
from backwork.direction import disrap
from backwork.fonctions import*
from IA.souvenirs import Souvenirs


class IA:
    def __init__(self):
        self.mots_clef = {'?Si':self.si_ia, '?Tant':self.tant_ia, '?Alea':self.alea_ia}
        self.mod_mots_clef = {'?Si':self.mod_si_ia, '?Tant':self.mod_tant_ia, '?Alea':self.mod_alea_ia}
        self.cree_m_clef = [self.cree_code_si_ia, self.cree_code_tant_ia,
                            self.cree_code_alea_ia]
        self.donnee = {':PVie': self.Vie_ia,':PTrue':self.True_ia}
        self.cree_donnee = {}
        #self.demarche = {'.Imite':self.Imite, '.Cibler':self.Cibler}
        self.act = ''
        self.arg = ''
        #self.strat = [[],[]]
        self.consept = []
        self.sens = []
        self.tactique = ['!C !Fuite', '!Suis .Imite', '!Alerte !C !Charge ?Tant(:PVie;!Gniap)', '!M !Charge !Rep','!M !Charge !N','!D','!Alerte']
        self.memory = []
        #self.fil = None
        self.consept = {}
    """ 
    def stats(self):
        print('act____:', self.act)
        print('strat__:v')
        for i,j in enumerate(self.strat[0]):
            print('-=-',j,':', self.strat[1][i])
        print('tact___:')
        for i, j in enumerate(self.tactique):
            print('-', i, ':' , j)
        print('memory_:v')
        for i in self.memory:
            print('-=-',i)
        print('consept:', self.consept)
    
    def agit(self):
        while self.act!='fin':
            print('---decode---')
            self.decode()
            print('--- agit ---')
            self.action(self.arg)
            input('------------')
    
    def reflexion(self, arg):
        self.action = self.rien
        if self.act == 'fin':
            self.memory.append(self.fil)
            self.ranger()
            self.act = self.compare()
            self.fil = Souvenirs(self)
        elif self.act=='':
            self.act = self.compare()
            self.fil = Souvenirs(self)
        else:
            self.decode

    def compare(self):
        self.cree_tampon()
        classement = self.tactique[:]
        for i in classement:
            i.compare_situation(self)
        classement.sort(key = lambda i:i.proche, reverse = True)
        classement = classement[:self.choix]
        for i in classement:
            i.compare_resultat(self)
        classement.sort(key = lambda i:i.estime, reverse = True)
        self.elue = classement[0]
        if randint(0, self.initiative)==0:
            self.elue = self.test(self.elue.act)
        return self.elue.act"""
            
            
    def decode(self):
        _tam=self.act.split(' ')
        if _tam[0]!='':
            if _tam[0][0]=='_':
                self.act=''
                for i in range(1,len(_tam)):
                    if _tam[i]!='':
                        self.act+=_tam[i]+' '
                self.decode()
            elif _tam[0][0]=='?':
                temp=_tam[0].split('(')
                act, cont = self.mots_clef[temp[0]](temp[1])
                if cont:
                    self.act=act+' '
                    for i in range(1,len(_tam)):
                        if _tam[i]!='':
                            self.act+=_tam[i]+' '
                else:
                    self.act=act+' !At '
                    for i in _tam:
                        if i!='':
                            self.act+=i+' '
                self.decode()
            elif _tam[0][0]=='!':
                self.arg = ''
                for i in _tam[0]:
                    if i == '{':
                        temp=_tam[0].split('{')
                        self.arg = temp[1]
                        _tam[0]=temp[0]
                self.action=self.base[_tam[0]]
                self.act=''
                for i in range(1,len(_tam)):
                    if _tam[i]!='':
                        self.act+=_tam[i]+' '
            elif _tam[0][0]=='.':
                self.arg = ''
                for i in _tam[0]:
                    if i == '{':
                        temp=_tam[0].split('{')
                        self.arg = temp[1]
                        _tam[0]=temp[0]
                self.action=self.demarche[_tam[0]]
                self.act=''
                for i in range(1,len(_tam)):
                    if _tam[i]!='':
                        self.act+=_tam[i]+' '
            else:
                _tam[0]=self.tactique[int(_tam[0])]
                self.act=''
                for i in range(len(_tam)):
                    if _tam[i]!='':
                        self.act+=_tam[i]+' '
                self.decode()
        else:
            self.act = ''
            self.action = self.rien
            self.arg = ''
            
        #! actions fondamantales

    #? mots clef
    def si_ia(self, arg):
        arg = arg.split(';')
        cond = arg[0]
        ret='_'
        condit = self.activ_donnee(cond)
            
        if condit:
            ret=''
            for i in range(len(arg[1])-1):
                ret+=arg[1][i]
        return ret, True
    
    def tant_ia(self, arg):
        arg = arg.split(';')
        cond = arg[0]
        ret='_'
        condit = self.activ_donnee(cond)
        cont = True
            
        if condit:
            cont = False
            ret=''
            for i in range(len(arg[1])-1):
                ret+=arg[1][i]
        return ret, cont
    
    def alea_ia(self, arg):
        arg = arg.split(';')
        i=randint(0, len(arg)-1)
        ret=''
        if i == len(arg)-1:
            for j in range(len(arg[i])-1):
                ret+=arg[i][j]
        else:
            ret=arg[i]
        return ret,True
    
    def cree_code_si_ia(self, arg):
        return('?Si('+self.alea_donnee()+';'+arg+')')
    
    def cree_code_tant_ia(self, arg):
        return('?Tant('+self.alea_donnee()+';'+arg+')')
    
    def cree_code_alea_ia(self, arg):
        return('?Alea('+arg+';'+self.act_alea()+')')
    
    def mod_si_ia(self, arg):
        arg = arg.split(';')
        return('?Si('+self.alea_donnee()+';'+arg[1])
    
    def mod_tant_ia(self, arg):
        arg = arg.split(';')
        return('?Tant('+self.alea_donnee()+';'+arg[1])
    
    def mod_alea_ia(self, arg):
        return('?Alea('+self.act_alea()+';'+arg)
    
    def cree_donnee_taille(self):
        l=randint(0,2)
        if l==0:
            r=''
        if l==1:
            r='>'
        if l==2:
            r='<'
        return(':NTaille'+'='+r+str(self.cible.taille)+')')
    #: donnee
    def activ_donnee(self, cond):
        if cond[0]==':':
            test = cond.split('=')
            if len(test)==2:
                if test[1][0]=='<':
                    r=''
                    for i in range(1,len(test[1])):
                        r+=test[1][i]
                    return(self.activ_donnee(test[0])<=self.activ_donnee(r))
                if test[1][0]=='>':
                    r=''
                    for i in range(1,len(test[1])):
                        r+=test[1][i]
                    return(self.activ_donnee(test[0])>=self.activ_donnee(r))    
                if test[1][0]=='n':
                    return(not self.activ_donnee(test[0]))
            else:
                if cond[1]=='P':
                    cond = cond.split('[')
                    if len(cond)==2:
                        return(self.donnee[cond[0]](cond[1]))
                    else:
                        return(self.donnee[cond[0]](''))
                elif cond[1]=='N':
                    cond = cond.split('[')
                    if len(cond)==2:
                        return(self.donnee[cond[0]](cond[1]))
                    else:
                        return(self.donnee[cond[0]](''))
                else:
                    r=''
                    for i in range(1,len(cond)):
                        r+=cond[i]
                    return(int(r))

    def Vie_ia(self, arg):
        if self.cible==None:
            return False
        else:
            if self.cible.reigne=='A':
                return self.cible.vie[0]>0
            else:
                return False
            
    
    def True_ia(self, arg):
        return(True)