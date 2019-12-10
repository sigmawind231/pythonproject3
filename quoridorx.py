from turtle import Turtle, Screen
from quoridor import Quoridor


class QuoridorX(Quoridor):
    tur = Turtle()
    loadwindow = Screen()

    def __init__(self, joueurs, murs = None):
        super().__init__(joueurs, murs)
        self.loadwindow.bgcolor('green')
        self.loadwindow.tracer(0)
        self.tur.speed(0)
        self.tur.hideturtle()
        self.afficher

    def afficher(self):
        self.tur.reset()

        dictio = self.infojeu
        posxj = dictio['joueurs'][0]['pos'][0]
        posyj = dictio['joueurs'][0]['pos'][1]
        posxa = dictio['joueurs'][1]['pos'][0]
        posya = dictio['joueurs'][1]['pos'][1]
        murshori = dictio['murs']['horizontaux']
        mursverti = dictio['murs']['verticaux']
        iden1 = dictio['joueurs'][0]['nom']
        iden2 = dictio['joueurs'][1]['nom']

        self.tur.color('red')
        self.tur.penup()
        self.tur.setx(-180)
        self.tur.sety(-180)
        self.tur.pendown()

        #Traçage de la grille
        for _ in range(4):
            self.tur.pensize(2)
            self.tur.fd(360)
            self.tur.lt(90)
        self.tur.pensize(1)
        for i in range(9):
            self.tur.penup()
            self.tur.setx(-180)
            self.tur.sety(-180 + (40*i))
            self.tur.pendown()
            self.tur.fd(360)
        for i in range(9):
            self.tur.penup()
            self.tur.sety(-180)
            self.tur.setx(-180 + (40*i))
            self.tur.pendown()
            self.tur.sety(180)
            self.tur.penup()

        #Traçage des numéros
        for i in range(9):
            self.tur.penup()
            self.tur.setpos(-160 + ((i)*40), -200)
            self.tur.color('white')
            self.tur.write(f'{i + 1}', font=('Arial', 10))
            self.tur.penup()
        for i in range(9):
            self.tur.penup()
            self.tur.setpos(-200 , -170 + ((i)*40))
            self.tur.color('white')
            self.tur.write(f'{i + 1}', font=('Arial', 10))
            self.tur.penup()

        #Positionnement des joueurs
        self.tur.setpos(-163 + (posxj-1)*40 , -170 + (posyj-1)*40)
        self.tur.color('white')
        self.tur.write('1', font=('Arial', 10))

        self.tur.setpos(-163 + (posxa-1)*40 , -170 + (posya-1)*40)
        self.tur.color('white')
        self.tur.write('2', font=('Arial', 10))

        #Positionnement des murs horizontaux
        for i in murshori:
            self.tur.penup()
            self.tur.setpos(-175 + (i[0]-1)*40 , -180 + (i[1]-1)*40)
            self.tur.color('black')
            self.tur.pensize(3)
            self.tur.pendown()
            self.tur.fd(70)

        #Positionnement des murs verticaux
        self.tur.lt(90)
        for i in mursverti:
            self.tur.penup()
            self.tur.setpos(-180 + (i[0]-1)*40, -175 + (i[1]-1)*40)
            self.tur.color('black')
            self.tur.pensize(3)
            self.tur.pendown()
            self.tur.fd(70)
        
        self.tur.penup()
        self.tur.setpos(-200 , 190)
        self.tur.color('white')
        self.tur.write('Légende: 1='f'{iden1}'', 2='f'{iden2}', font=('Arial', 10))
        self.tur.penup()
        #Ajout de la légende