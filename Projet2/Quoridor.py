infojeu = {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 6]},
        {"nom": "automate", "murs": 3, "pos": [5, 7]}
    ],
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]],
        "verticaux": [[6, 2], [4, 4], [2, 5], [7, 5], [7, 7]]
    }
}


class Quoridor:

    def __init__(self, joueurs, murs=None):
        """
        Initialiser une partie de Quoridor avec les joueurs et les murs spécifiés, 
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.

        :param joueurs: un itérable de deux joueurs dont le premier est toujours celui qui 
        débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire. 
        Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans 
        l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut initialement
        placer 10 murs. Dans le cas où l'argument est un dictionnaire, celui-ci doit contenir 
        une clé 'nom' identifiant le joueur, une clé 'murs' spécifiant le nombre de murs qu'il 
        peut encore placer, et une clé 'pos' qui spécifie sa position (x, y) actuelle.
        
        :param murs: un dictionnaire contenant une clé 'horizontaux' associée à la liste des
        positions (x, y) des murs horizontaux, et une clé 'verticaux' associée à la liste des
        positions (x, y) des murs verticaux. Par défaut, il n'y a aucun mur placé sur le jeu.

        :raises QuoridorError: si l'argument 'joueurs' n'est pas itérable.
        :raises QuoridorError: si l'itérable de joueurs en contient plus de deux.
        :raises QuoridorError: si le nombre de murs qu'un joueur peut placer est >10, ou négatif.
        :raises QuoridorError: si la position d'un joueur est invalide.
        :raises QuoridorError: si l'argument 'murs' n'est pas un dictionnaire lorsque présent.
        :raises QuoridorError: si le total des murs placés et plaçables n'est pas égal à 20.
        :raises QuoridorError: si la position d'un mur est invalide.
        """

    def __str__(self):
        """Permet de convertir un dictionnaire en damier ascii"""
        lignes = []
        lignes += list("Légende: 1="+ str(infojeu["joueurs"][0]["nom"])+
                    ', 2='+str(infojeu["joueurs"][1]["nom"]) + "\n")
        lignes += list("   "+"-"*35+"\n")
        for i in range(1, 10):
            lignes += str(10-i) + " | "
            for j in range(1, 9):
                strplayer = "."
                if [j, 10-i] == infojeu["joueurs"][0]["pos"]:
                    strplayer = "1"
                elif [j, 10-i] == infojeu["joueurs"][1]["pos"]:
                    strplayer = "2"
                if [j+1, 10-i] in infojeu["murs"]["verticaux"]:
                    lignes += list(strplayer + " | ")
                elif [j+1, 9-i] in infojeu["murs"]["verticaux"]:
                    lignes += list(strplayer + " | ")
                else:
                    lignes += list(strplayer + "   ")
            if [9, 10-i] == infojeu["joueurs"][0]["pos"]:
                lignes += list("1 |")
            elif [9, 10-i] == infojeu["joueurs"][1]["pos"]:
                lignes += list("2 |")
            else:
                lignes += list(". |")
            if i != 9:
                lignes += list("\n  |")
            for k in range(1, 9):
                if i != 9:
                    if [k, 10-i] in infojeu["murs"]["horizontaux"]:
                        lignes += list("----")
                    elif [k-1, 10-i] in infojeu["murs"]["horizontaux"] and \
                        [k+1, 9-i] in infojeu["murs"]["verticaux"]:
                        lignes += list("---|")
                    elif [k-1, 10-i] in infojeu["murs"]["horizontaux"]:
                        lignes += list("--- ")
                    elif [k+1, 9-i] in infojeu["murs"]["verticaux"]:
                        lignes += list("   |")
                    else:
                        lignes += list("    ")
            if i != 9:
                if [8, 10-i] in infojeu["murs"]["horizontaux"]:
                    lignes += list("---|")
                else:
                    lignes += list("   |")
            lignes += list("\n")
        lignes += list("--|"+ "-"*35+"\n")
        lignes += list("  | 1   2   3   4   5   6   7   8   9")
        lignes = ''.join(lignes)
        print(lignes)
    
    def déplacer_jeton(self, joueur, position):
        """
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :param position: le tuple (x, y) de la position du jeton (1<=x<=9 et 1<=y<=9).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la position est invalide (en dehors du damier).
        :raises QuoridorError: si la position est invalide pour l'état actuel du jeu.
        """
        pass

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
        pass

    def jouer_coup(self, joueur):
        """
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel 
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un 
        mur horizontal ou vertical.

        :param joueur: un entier spécifiant le numéro du joueur (1 ou 2).
        :raises QuoridorError: si le numéro du joueur est autre que 1 ou 2.
        :raises QuoridorError: si la partie est déjà terminée.
        """
        pass
    def partie_terminée(self):
        """
        Déterminer si la partie est terminée.

        :returns: le nom du gagnant si la partie est terminée; False autrement.
        """
        joueur1 = infojeu['joueurs'][0]['nom']
        pos1 = infojeu['joueurs'][0]['pos'][1]
        joueur2 = infojeu['joueurs'][1]['nom']
        pos2 = infojeu['joueurs'][1]['pos'][1]
        if pos1 == 9:
            return joueur1
        if pos2 == 1:
            return joueur2
        else:
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
        pass
