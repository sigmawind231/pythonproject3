import turtle as tur
from quoridor import Quoridor


class QuoridorX(Quoridor):

    def __init__(self, joueurs, murs = None):
        super().__init__(joueurs, murs)
        loadwindow = tur.Screen()
        loadwindow.bgcolor('green')
        tur.speed(0)
        tur.hideturtle()
        self.afficher

    def afficher(self):
        tur.reset()
        tur.tracer(0)

        dictio = self.infojeu
        posxj = dictio['joueurs'][0]['pos'][0]
        posyj = dictio['joueurs'][0]['pos'][1]
        posxa = dictio['joueurs'][1]['pos'][0]
        posya = dictio['joueurs'][1]['pos'][1]
        murshori = dictio['murs']['horizontaux']
        mursverti = dictio['murs']['verticaux']
        iden1 = dictio['joueurs'][0]['nom']
        iden2 = dictio['joueurs'][1]['nom']

        tur.color('red')
        tur.penup()
        tur.setx(-180)
        tur.sety(-180)
        tur.pendown()

        #Traçage de la grille
        for _ in range(4):
            tur.pensize(2)
            tur.fd(360)
            tur.lt(90)
        tur.pensize(1)
        for i in range(9):
            tur.penup()
            tur.setx(-180)
            tur.sety(-180 + (40*i))
            tur.pendown()
            tur.fd(360)
        for i in range(9):
            tur.penup()
            tur.sety(-180)
            tur.setx(-180 + (40*i))
            tur.pendown()
            tur.sety(180)
            tur.penup()

        #Traçage des numéros
        for i in range(9):
            tur.penup()
            tur.setpos(-160 + ((i)*40), -200)
            tur.color('white')
            tur.write(f'{i + 1}', font=('Arial', 10))
            tur.penup()
        for i in range(9):
            tur.penup()
            tur.setpos(-200 , -170 + ((i)*40))
            tur.color('white')
            tur.write(f'{i + 1}', font=('Arial', 10))
            tur.penup()

        #Positionnement des joueurs
        tur.setpos(-163 + (posxj-1)*40 , -170 + (posyj-1)*40)
        tur.color('white')
        tur.write('1', font=('Arial', 10))

        tur.setpos(-163 + (posxa-1)*40 , -170 + (posya-1)*40)
        tur.color('white')
        tur.write('2', font=('Arial', 10))

        #Positionnement des murs horizontaux
        for i in murshori:
            tur.penup()
            tur.setpos(-175 + (i[0]-1)*40 , -180 + (i[1]-1)*40)
            tur.color('black')
            tur.pensize(3)
            tur.pendown()
            tur.fd(70)

        #Positionnement des murs verticaux
        tur.lt(90)
        for i in mursverti:
            tur.penup()
            tur.setpos(-180 + (i[0]-1)*40, -175 + (i[1]-1)*40)
            tur.color('black')
            tur.pensize(3)
            tur.pendown()
            tur.fd(70)
        
        tur.penup()
        tur.setpos(-200 , 190)
        tur.color('white')
        tur.write('Légende: 1='f'{iden1}'', 2='f'{iden2}', font=('Arial', 10))
        tur.penup()
        #Ajout de la légende