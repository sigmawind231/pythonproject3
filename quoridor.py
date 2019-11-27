'''module quoridor'''


import random as rnd
import networkx as nx


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs."""
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))
    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # retirer tous les arcs qui pointent vers les positions des joueurs
    # et ajouter les sauts en ligne droite ou en diagonale, selon le cas
    for joueur in map(tuple, joueurs):

        for prédécesseur in list(graphe.predecessors(joueur)):
            graphe.remove_edge(prédécesseur, joueur)

            # si admissible, ajouter un lien sauteur
            successeur = (2*joueur[0]-prédécesseur[0], 2*joueur[1]-prédécesseur[1])

            if successeur in graphe.successors(joueur) and successeur not in joueurs:
                # ajouter un saut en ligne droite
                graphe.add_edge(prédécesseur, successeur)

            else:
                # ajouter les liens en diagonal
                for successeur in list(graphe.successors(joueur)):
                    if prédécesseur != successeur and successeur not in joueurs:
                        graphe.add_edge(prédécesseur, successeur)

    # ajouter les noeuds objectifs des deux joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe


class QuoridorError(Exception):
    '''QuoridorError'''


class Quoridor:
    '''Quoridor'''

    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.
        """
        if not hasattr(joueurs, '__iter__'):
            raise QuoridorError
        if len(joueurs) > 2:
            raise QuoridorError
        if isinstance(joueurs[0], str):
            dictp1 = {"nom": joueurs[0], "murs": 10, "pos": [5, 1]}
        else:
            dictp1 = joueurs[0]
        if isinstance(joueurs[1], str):
            dictp2 = {"nom": joueurs[1], "murs": 10, "pos": [5, 9]}
        else:
            dictp2 = joueurs[1]
        if murs is None:
            murs = {"horizontaux": [], "verticaux": []}
        elif not isinstance(murs, dict):
            raise QuoridorError
        self.infojeu = {"joueurs": [dictp1, dictp2], "murs": murs}
        if self.infojeu["joueurs"][0]["murs"] > 10 or self.infojeu["joueurs"][0]["murs"] < 0:
            raise QuoridorError
        if self.infojeu["joueurs"][1]["murs"] > 10 or self.infojeu["joueurs"][1]["murs"] < 0:
            raise QuoridorError
        if self.infojeu["joueurs"][0]["pos"][0] < 1 or self.infojeu["joueurs"][0]["pos"][0] > 9:
            raise QuoridorError
        if self.infojeu["joueurs"][0]["pos"][1] < 1 or self.infojeu["joueurs"][0]["pos"][1] > 9:
            raise QuoridorError
        if self.infojeu["joueurs"][1]["pos"][0] < 1 or self.infojeu["joueurs"][1]["pos"][0] > 9:
            raise QuoridorError
        if self.infojeu["joueurs"][1]["pos"][1] < 1 or self.infojeu["joueurs"][1]["pos"][1] > 9:
            raise QuoridorError
        a = self.infojeu["joueurs"][0]["murs"] + self.infojeu["joueurs"][1]["murs"]
        b = len(self.infojeu["murs"]["horizontaux"]) + len(self.infojeu["murs"]["verticaux"])
        if  (a + b) != 20:
            raise QuoridorError
        for j, valeur in enumerate(self.infojeu['murs']['horizontaux']):
            posx = valeur[0]
            posy = valeur[1]
            for i, value in enumerate(self.infojeu['murs']['horizontaux']):
                if (value[0] == posx and value[1] == posy) and i != j:
                    raise QuoridorError
                elif (value[0] == posx+1 or value[0] == posx-1) and value[1] == posy:
                    raise QuoridorError
                elif posx >= 9 or posx < 1:
                    raise QuoridorError
                elif posy <= 1 or posy > 9:
                    raise QuoridorError
            for i, value in enumerate(self.infojeu['murs']['verticaux']):
                if value[0] == posx+1 and value[1] == posy - 1:
                    print(value)
                    print((posx, posy))
                    raise QuoridorError
        for j, valeur in enumerate(self.infojeu['murs']['verticaux']):
            posx = valeur[0]
            posy = valeur[1]
            for i, value in enumerate(self.infojeu['murs']['verticaux']):
                if value[0] == posx and value[1] == posy and i != j:
                    raise QuoridorError
                elif (value[1] == posy-1 or value[1] == posy+1) and value[0] == posx:
                    raise QuoridorError
                elif posy >= 9 or posy < 1:
                    raise QuoridorError
                elif posx <= 1 or posx > 9:
                    raise QuoridorError
            for i, value in enumerate(self.infojeu['murs']['horizontaux']):
                if value[0] == posx-1 and value[1] == posy+1:
                    raise QuoridorError

    def __str__(self):
        """
        Produire la représentation en art ascii correspondant à l'état actuel de la partie.
        Cette représentation est la même que celle du TP précédent.

        :returns: la chaîne de caractères de la représentation.
        """
        lignes = []
        lignes += list("Légende: 1="+ str(self.infojeu["joueurs"][0]["nom"])+
                       ', 2='+str(self.infojeu["joueurs"][1]["nom"]) + "\n")
        lignes += list("   "+"-"*35+"\n")
        for i in range(1, 10):
            lignes += str(10-i) + " | "
            for j in range(1, 9):
                strplayer = "."
                if [j, 10-i] == self.infojeu["joueurs"][0]["pos"]:
                    strplayer = "1"
                elif [j, 10-i] == self.infojeu["joueurs"][1]["pos"]:
                    strplayer = "2"
                if [j+1, 10-i] in self.infojeu["murs"]["verticaux"]:
                    lignes += list(strplayer + " | ")
                elif [j+1, 9-i] in self.infojeu["murs"]["verticaux"]:
                    lignes += list(strplayer + " | ")
                else:
                    lignes += list(strplayer + "   ")
            if [9, 10-i] == self.infojeu["joueurs"][0]["pos"]:
                lignes += list("1 |")
            elif [9, 10-i] == self.infojeu["joueurs"][1]["pos"]:
                lignes += list("2 |")
            else:
                lignes += list(". |")
            if i != 9:
                lignes += list("\n  |")
            for k in range(1, 9):
                if i != 9:
                    if [k, 10-i] in self.infojeu["murs"]["horizontaux"]:
                        lignes += list("----")
                    elif [k-1, 10-i] in self.infojeu["murs"]["horizontaux"] and \
                        [k+1, 9-i] in self.infojeu["murs"]["verticaux"]:
                        lignes += list("---|")
                    elif [k-1, 10-i] in self.infojeu["murs"]["horizontaux"]:
                        lignes += list("--- ")
                    elif [k+1, 9-i] in self.infojeu["murs"]["verticaux"]:
                        lignes += list("   |")
                    else:
                        lignes += list("    ")
            if i != 9:
                if [8, 10-i] in self.infojeu["murs"]["horizontaux"]:
                    lignes += list("---|")
                else:
                    lignes += list("   |")
            lignes += list("\n")
        lignes += list("--|"+ "-"*35+"\n")
        lignes += list("  | 1   2   3   4   5   6   7   8   9")
        lignes = ''.join(lignes)
        return lignes

    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """

        jfonction = [self.infojeu['joueurs'][0]['pos'], self.infojeu['joueurs'][1]['pos']]
        mhfonction = self.infojeu['murs']['horizontaux']
        mvfonction = self.infojeu['murs']['verticaux']
        if joueur != 1 and joueur != 2:
            raise QuoridorError
        elif 9 < position[0] < 1:
            raise QuoridorError
        elif 9 < position[1] < 1:
            raise QuoridorError
        elif position not in construire_graphe(jfonction, mhfonction, mvfonction).successors(tuple(self.infojeu['joueurs'][joueur - 1]['pos'])):
            raise QuoridorError
        self.infojeu['joueurs'][joueur - 1]['pos'] = list(position)

    def état_partie(self):
        """
        Produire l'état actuel de la partie.

        :returns: une copie de l'état actuel du jeu sous la forme d'un dictionnaire:
        {
            'joueurs': [
                {'nom': nom1, 'murs': n1, 'pos': (x1, y1)},
                {'nom': nom2, 'murs': n2, 'pos': (x2, y2)},
            ],
            'murs': {
                'horizontaux': [...],
                'verticaux': [...],
            }
        }

        où la clé 'nom' d'un joueur est associée à son nom, la clé 'murs' est associée
        au nombre de murs qu'il peut encore placer sur ce damier, et la clé 'pos' est
        associée à sa position sur le damier. Une position est représentée par un tuple
        de deux coordonnées x et y, où 1<=x<=9 et 1<=y<=9.

        Les murs actuellement placés sur le damier sont énumérés dans deux listes de
        positions (x, y). Les murs ont toujours une longueur de 2 cases et leur position
        est relative à leur coin inférieur gauche. Par convention, un mur horizontal se
        situe entre les lignes y-1 et y, et bloque les colonnes x et x+1. De même, un
        mur vertical se situe entre les colonnes x-1 et x, et bloque les lignes y et y+1.
        """
        return self.infojeu

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """
        if joueur != 1 and joueur != 2:
            raise QuoridorError
        if not self.partie_terminée:
            raise QuoridorError
        jfonction = [self.infojeu['joueurs'][0]['pos'], self.infojeu['joueurs'][1]['pos']]
        mhfonction = self.infojeu['murs']['horizontaux']
        mvfonction = self.infojeu['murs']['verticaux']
        choix = rnd.choice([True, False])
        if self.infojeu['joueurs'][joueur-1]['murs'] == 0:
            choix = True
        posrandom = rnd.choice(list(construire_graphe(jfonction, mhfonction, mvfonction).successors(tuple(self.infojeu['joueurs'][joueur - 1]['pos']))))
        if choix is True:
            while isinstance(posrandom, str):
                posrandom = rnd.choice(list(construire_graphe(jfonction, mhfonction, mvfonction).successors(tuple(self.infojeu['joueurs'][joueur - 1]['pos']))))
            self.déplacer_jeton(joueur, posrandom)
        if choix is False:
            haserror = True
            while haserror == True:
                lignex = rnd.randint(1, 9)
                colonney = rnd.randint(1, 9)
                orientationrand = rnd.choice(["horizontal", "vertical"])
                try:
                    self.placer_mur(joueur, (lignex, colonney), orientationrand)
                    haserror = False
                except QuoridorError as err:
                    print(err)
                    haserror = True

    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        joueur1 = self.infojeu['joueurs'][0]['nom']
        pos1 = self.infojeu['joueurs'][0]['pos'][1]
        joueur2 = self.infojeu['joueurs'][1]['nom']
        pos2 = self.infojeu['joueurs'][1]['pos'][1]
        if pos1 == 9:
            return joueur1
        if pos2 == 1:
            return joueur2
        return False

    def placer_mur(self, joueur, position, orientation):
        """
        Pour le joueur spécifié, placer un mur à la position spécifiée.

        :param joueur: le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du mur.
        :param orientation: l'orientation du mur ('horizontal' ou 'vertical').
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si un mur occupe déjà cette position.
        :raises QuoridorError: si la position est invalide pour cette orientation.
        :raises QuoridorError: si le joueur a déjà placé tous ses murs.
        """
        posx = position[0]
        posy = position[1]
        modificationdirection = ''
        if self.infojeu['joueurs'][joueur-1]['murs'] == 0:
            raise QuoridorError
        elif joueur == 1 or joueur == 2:
            if orientation == 'horizontal':
                modificationdirection = 'horizontaux'
                for i, value in enumerate(self.infojeu['murs']['horizontaux']):
                    if value[0] == posx and value[1] == posy:
                        raise QuoridorError
                    elif (value[0] == posx+1 or value[0] == posx-1) and value[1] == posy:
                        raise QuoridorError
                    elif posx >= 9 or posx < 1:
                        raise QuoridorError
                    elif posy <= 1 or posy > 9:
                        raise QuoridorError
                for i, value in enumerate(self.infojeu['murs']['verticaux']):
                    if value[0] == posx+1 and value[1] == posy-1:
                        raise QuoridorError
            elif orientation == 'vertical':
                modificationdirection = 'verticaux'
                for i, value in enumerate(self.infojeu['murs']['verticaux']):
                    if value[0] == posx and value[1] == posy:
                        raise QuoridorError
                    elif (value[1] == posy-1 or value[1] == posy+1) and value[0] == posx:
                        raise QuoridorError
                    elif posy >= 9 or posy < 1:
                        raise QuoridorError
                    elif posx <= 1 or posx > 9:
                        raise QuoridorError
                for i, value in enumerate(self.infojeu['murs']['horizontaux']):
                    if value[0] == posx-1 and value[1] == posy+1:
                        raise QuoridorError
        else:
            raise QuoridorError
        jfonction = [self.infojeu['joueurs'][0]['pos'], self.infojeu['joueurs'][1]['pos']]
        mhfonction = self.infojeu['murs']['horizontaux']
        mvfonction = self.infojeu['murs']['verticaux']
        graphe = construire_graphe(jfonction, mhfonction, mvfonction)
        self.infojeu['murs'][modificationdirection].append([posx, posy])
        if joueur == 1:
            if not nx.has_path(graphe, tuple(self.infojeu['joueurs'][joueur-1]['pos']), 'B1'):
                self.infojeu['murs'][modificationdirection].pop()
                raise QuoridorError
        else:
            if not nx.has_path(graphe, tuple(self.infojeu['joueurs'][joueur-1]['pos']), 'B2'):
                self.infojeu['murs'][modificationdirection].pop()
                raise QuoridorError
        self.infojeu['joueurs'][joueur-1]['murs'] -= 1

joueurs = [
        {"nom": "idul", "murs": 7, "pos": [5, 1]},
        {"nom": "automate", "murs": 3, "pos": [5, 9]}
    ]
murstest = {"horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
            "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]}
test1 = Quoridor(joueurs, murstest)
print(test1)
test1.jouer_coup(1)
print(test1)
test1.jouer_coup(2)
print(test1)
test1.jouer_coup(1)
print(test1)
test1.jouer_coup(2)
print(test1)
test1.jouer_coup(1)
print(test1)
test1.jouer_coup(2)
print(test1)
test1.jouer_coup(1)
print(test1)
test1.jouer_coup(2)
print(test1)
test1.jouer_coup(1)
print(test1)
test1.jouer_coup(2)
print(test1)
test1.jouer_coup(1)
print(test1)
test1.jouer_coup(2)


##print(infojeu["joueurs"][0]["murs"] + infojeu["joueurs"][1]["murs"] + len(infojeu["murs"]["horizontaux"]) + len(infojeu["murs"]["verticaux"]))
