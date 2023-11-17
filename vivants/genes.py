from random import randint

def protozoide():
    return  [[
            [1,0.1, 0.02],#vitesse
            [1,0.1, 0.01],#vie max
            [1,0.1, 0.01],#regen
            [1,0, 0.001], #rotation
            [25, 0.02, 0.001], #esperance de vie
            [1, 0.1, 0.001] #reserve
        ], [
            [1, 0.1, 0.001],  # taille de l'estomac
            [1, 0.1, 0.005], # vitesse de repas
            [1, 0, 0], #alerte: faim
            [1, 0, 0] #faim
        ],[
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0]
        ],[
            [4, 0.001, 0.01]
        ]]

def aleatoires():
    return [[[randint(1,3),0.1, 0.02],#vitesse
            [randint(1,3),0.1, 0.01],#vie max
            [randint(1,3),0.1, 0.01],#regen
            [randint(1,3),0, 0.001], #rotation
            [randint(20,30), 0.02, 0.001], #esperance de vie
            [randint(1,3), 0.1, 0.001] #reserve
        ], [
            [randint(1,5), 0.1, 0.001],  # taille de l'estomac
            [randint(1,3), 0.1, 0.005], # vitesse de repas
            [randint(1,3), 0, 0], #faim
            [randint(1,3), 0, 0] #alerte faim
        ],[
            [randint(1,10), 0, 0] for _ in range(11)
        ],[
            [randint(5,10), 0.001, 0.01]
            ]]

def apparente(parent1, parent2):
    return  [[
            ordre(parent1.orga[0].potentiel[0][0], parent2.orga[0].potentiel[0][0],0.1, 0.02),#vitesse
            ordre(parent1.orga[0].potentiel[1][0], parent2.orga[0].potentiel[1][0],0.1, 0.01),#vie max
            ordre(parent1.orga[0].potentiel[2][0], parent2.orga[0].potentiel[2][0],0.1, 0.01),#regen
            ordre(parent1.orga[0].potentiel[3][0], parent2.orga[0].potentiel[3][0],0, 0.001), #rotation
            ordre(parent1.orga[0].potentiel[4][0], parent2.orga[0].potentiel[4][0], 0.1, 0.001), #esperance de vie
            ordre(parent1.orga[0].potentiel[5][0], parent2.orga[0].potentiel[5][0], 0.1, 0.001), #reserve
        ], [ #estomac
            ordre(parent1.orga[1].potentiel[0][0], parent2.orga[1].potentiel[0][0], 0.1, 0.001),
            ordre(parent1.orga[1].potentiel[1][0], parent2.orga[1].potentiel[1][0], 0.1, 0.005), #vitesse de consomation
            ordre(parent1.orga[1].potentiel[2][0], parent2.orga[1].potentiel[2][0], 0, 0),
            ordre(parent1.orga[1].potentiel[3][0], parent2.orga[1].potentiel[3][0], 0, 0)
        ], [
            ordre(parent1.orga[2].potentiel[i][0], parent2.orga[2].potentiel[i][0], 0, 0) for i in range(11)
        ], [
            ordre(parent1.orga[3].potentiel[0][0], parent2.orga[3].potentiel[0][0], 0, 0)
        ]
            ]

def ordre(a,b,sec1, sec2):
    if a>b:
        if b>1:
            return[randint(b-1, a+1), sec1, sec2]
        else:
            return[randint(b, a+1), sec1, sec2]
    else:
        if a>1:
            return[randint(a-1, b+1), sec1, sec2]
        else:
            return[randint(a, b+1), sec1, sec2]