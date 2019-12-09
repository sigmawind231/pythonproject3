'''module quoridor'''

import copy
import random as rnd
import networkx as nx


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """
    Crée le graphe des déplacements admissibles pour les joueurs.

    :param joueurs: une liste des positions (x,y) des joueurs.
    :param murs_horizontaux: une liste des positions (x,y) des murs horizontaux.
    :param murs_verticaux: une liste des positions (x,y) des murs verticaux.
    :returns: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
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

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
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

        """Produire la représentation en art ascii"""
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

        """Pour le joueur spécifié, déplacer son jeton à la position spécifiée."""

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

        """Produire l'état actuel de la partie."""

        return self.infojeu

    def jouer_coup(self, joueur):

        """Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical."""

        if joueur != 1 and joueur != 2:
            raise QuoridorError
        if not self.partie_terminée:
            raise QuoridorError
        opposant = 2
        if joueur == 2:
            opposant = 1
            
        jfonction = [self.infojeu['joueurs'][0]['pos'], self.infojeu['joueurs'][1]['pos']]
        mhfonction = self.infojeu['murs']['horizontaux']
        mvfonction = self.infojeu['murs']['verticaux']
        resteMurs = True
        if self.infojeu['joueurs'][joueur-1]['murs'] == 0:
            resteMurs = False
        graph = construire_graphe(jfonction, mhfonction, mvfonction)
        if nx.shortest_path_length(graph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur)) < nx.shortest_path_length(graph, tuple(self.infojeu['joueurs'][opposant - 1]['pos']), "B"+str(opposant)):
            path = nx.shortest_path(graph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
            self.déplacer_jeton(joueur, path[1])
        elif resteMurs:
            shortestPathOpposant = nx.shortest_path_length(graph, tuple(self.infojeu['joueurs'][opposant - 1]['pos']), "B"+str(opposant))
            shortestPathJoueur = nx.shortest_path_length(graph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
            lenghtMur = shortestPathOpposant - shortestPathJoueur
            posMur = [0,0]
            orientation = 'horizontal'
            for i in range(1, 10):
                for j in range(1, 10):
                    modified = copy.deepcopy(mhfonction)
                    modified.append([i, j])
                    try:
                        newgraph = construire_graphe(jfonction, modified, mvfonction)
                        shortestPathOpposant = nx.shortest_path_length(newgraph, tuple(self.infojeu['joueurs'][opposant - 1]['pos']), "B"+str(opposant))
                        shortestPathJoueur = nx.shortest_path_length(newgraph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
                        hasPathOpposant = nx.has_path(newgraph, tuple(self.infojeu['joueurs'][opposant - 1]['pos']), "B"+str(opposant))
                        hasPathJoueur = nx.has_path(newgraph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
                        if (shortestPathOpposant - shortestPathJoueur) > lenghtMur and hasPathJoueur and hasPathOpposant:
                            posMur = [i, j]
                            lenghtMur = shortestPathOpposant - shortestPathJoueur
                    except:
                        pass
            for i in range(1, 10):
                for j in range(1, 10):
                    modified = copy.deepcopy(mvfonction)
                    modified.append([i, j])
                    try:
                        newgraph = construire_graphe(jfonction, mhfonction, modified)
                        shortestPathOpposant = nx.shortest_path_length(newgraph, tuple(self.infojeu['joueurs'][opposant - 1]['pos']), "B"+str(opposant))
                        shortestPathJoueur = nx.shortest_path_length(newgraph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
                        hasPathOpposant = nx.has_path(newgraph, tuple(self.infojeu['joueurs'][opposant - 1]['pos']), "B"+str(opposant))
                        hasPathJoueur = nx.has_path(newgraph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
                        if (shortestPathOpposant - shortestPathJoueur) > lenghtMur and hasPathJoueur and hasPathOpposant:
                            posMur = [i, j]
                            lenghtMur = shortestPathOpposant - shortestPathJoueur
                            orientation = 'vertical'
                    except:
                        pass
            if posMur == [0, 0]:
                path = nx.shortest_path(graph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
                self.déplacer_jeton(joueur, path[1])
            else:
                self.placer_mur(joueur, posMur, orientation)
        else:
            path = nx.shortest_path(graph, tuple(self.infojeu['joueurs'][joueur - 1]['pos']), "B"+str(joueur))
            self.déplacer_jeton(joueur, path[1])

    def partie_terminée(self):

        """Déterminer si la partie est terminée."""

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

        """Pour le joueur spécifié, placer un mur à la position spécifiée."""

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
