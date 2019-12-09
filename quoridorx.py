import turtle as t


dictio = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [1, 5]}, 
        {"nom": "automate", "murs": 3, "pos": [8, 6]}
    ], 
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]], 
        "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
    }
}









def afficher(dictio):

    posxj = dictio['joueurs'][0]['pos'][0]
    posyj = dictio['joueurs'][0]['pos'][1]
    posxa = dictio['joueurs'][1]['pos'][0]
    posya = dictio['joueurs'][1]['pos'][1]
    murshori = dictio['murs']['horizontaux']
    mursverti = dictio['murs']['verticaux']
    iden1 = dictio['joueurs'][0]['nom']
    iden2 = dictio['joueurs'][1]['nom']

    loadwindow = t.Screen()
    loadwindow.bgcolor('green')
    t.speed(0)
    t.hideturtle()

    t.color('red')
    t.penup()
    t.setx(-180)
    t.sety(-180)
    t.pendown()

    #Traçage de la grille
    for _ in range(4):
        t.pensize(2)
        t.fd(360)
        t.lt(90)
    t.pensize(1)
    for i in range(9):
        t.penup()
        t.setx(-180)
        t.sety(-180 + (40*i))
        t.pendown()
        t.fd(360)
    for i in range(9):
        t.penup()
        t.sety(-180)
        t.setx(-180 + (40*i))
        t.pendown()
        t.sety(180)
        t.penup()

    #Traçage des numéros
    for i in range(9):
        t.penup()
        t.setpos(-160 + ((i)*40), -200)
        t.color('white')
        t.write(f'{i + 1}', font=('Arial', 10))
        t.penup()
    for i in range(9):
        t.penup()
        t.setpos(-200 , -170 + ((i)*40))
        t.color('white')
        t.write(f'{i + 1}', font=('Arial', 10))
        t.penup()

    #Positionnement des joueurs
    t.setpos(-163 + (posxj-1)*40 , -170 + (posyj-1)*40)
    t.color('white')
    t.write('1', font=('Arial', 10))

    t.setpos(-163 + (posxa-1)*40 , -170 + (posya-1)*40)
    t.color('white')
    t.write('2', font=('Arial', 10))

    #Positionnement des murs horizontaux
    for i in murshori:
        t.penup()
        t.setpos(-175 + (i[0]-1)*40 , -180 + (i[1]-1)*40)
        t.color('black')
        t.pensize(3)
        t.pendown()
        t.fd(70)


    #Positionnement des murs verticaux
    t.lt(90)
    for i in mursverti:
        t.penup()
        t.setpos(-180 + (i[0]-1)*40, -175 + (i[1]-1)*40)
        t.color('black')
        t.pensize(3)
        t.pendown()
        t.fd(70)
    
    t.penup()
    t.setpos(-200 , 190)
    t.color('white')
    t.write('Légende: 1='f'{iden1}'', 2='f'{iden2}', font=('Arial', 10))
    t.penup()
    #Ajout de la légende

    t.exitonclick()
    

afficher(dictio)