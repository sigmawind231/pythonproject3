DICTIO = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 6]},
        {"nom": "automate", "murs": 3, "pos": [5, 7]}
    ],
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
    }
}



def afficher_damier_ascii(dictio):
                """affichage du damier"""
                #définition de la grille de base
                frame = [[' ' for i in range(39)] for j in range(20)]
                for j in range(20):
                    for i in range(39):
                        if j == 0 and 2 < i < 38:
                            frame[j][i] = '-'
                        elif j == 18 and i < 38 and i != 2:
                            frame[j][i] = '-'
                        elif i == 2 or i == 38:
                            frame[j][i] = '|'
                            frame[0][i] = ' '
                            frame[18][38] = frame[19][38] = ' '
                        elif i == 0 and j % 2 != 0 and j < 18:
                            frame[j][i] = f'{int(10 - j / 2)}'
                        elif j == 19 and i % 4 == 0 and 3 < i < 37:
                            frame[j][i] = f'{int(i / 4)}'
                        elif i % 4 == 0 and j % 2 != 0 and i > 0:
                            frame[j][i] = '.'

                #positionnement des joueurs
                pos_x_1 = (4 * dictio['joueurs'][0]['pos'][0])
                pos_y_1 = 19 - (2 * dictio['joueurs'][0]['pos'][1])
                pos_x_2 = (4 * dictio['joueurs'][1]['pos'][0])
                pos_y_2 = 19 - (2 * dictio['joueurs'][1]['pos'][1])
                frame[pos_y_1][pos_x_1] = '1'
                frame[pos_y_2][pos_x_2] = '2'

                #positionnement des murs verticaux
                for pos in dictio['murs']['verticaux']:
                    if pos[1] < 9:
                        x_v = pos[0] * 4
                        y_v = 19 - 2 * pos[1]
                        x_mur_milieu_v = int((x_v + (pos[0] - 1) * 4) / 2)
                        y_mur_milieu_v = int((y_v + (19 - 2 * (pos[1] + 1))) / 2)
                        frame[y_mur_milieu_v][x_mur_milieu_v] = '|'
                        frame[y_mur_milieu_v - 1][x_mur_milieu_v] = '|'
                        frame[y_mur_milieu_v + 1][x_mur_milieu_v] = '|'
                    else: break

                #positionnement des murs horizontaux
                for pos in dictio['murs']['horizontaux']:
                    if pos[0] <= 8:
                        x_h = pos[0] * 4
                        y_h = 19 - 2 * pos[1]
                        y_mur_milieu_h = int((y_h + (19 - 2 * (pos[1] - 1))) / 2)
                        for i in range(x_h - 1, ((pos[0] + 1) * 4) + 2):
                            frame[y_mur_milieu_h][i] = '-'
                    else: break

                #assemblage final du tableau
                for i in range(0, 20):
                    frame[i] = ''.join(frame[i])
                damier = '\n'.join(frame)

                #ajout de la légende
                damier_finale = f'Légende: 1={IDUL}, 2=automate' + '\n' + f'{damier}'
                print(damier_finale)
afficher_damier_ascii(DICTIO)