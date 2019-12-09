"""Module principal du jeu"""
import argparse
import copy

from quoridor import Quoridor
from api import débuter_partie, jouer_coup


def analyser_commande():
    """Permet d'utiliser la command line"""
    parser = argparse.ArgumentParser(
        description="Jeu Quoridor - phase 3")
    parser.add_argument(dest='idul', type=str, help="IDUL du joueur.")
    parser.add_argument("-a", "--automatique", dest='auto',
                        action="store_true",
                        help="Activer le mode automatique.")
    parser.add_argument("-x", "--graphique", dest='graph',
                        action="store_true",
                        help="Activer le mode graphique.")
    args = parser.parse_args()
    return args

def afficher_damier_ascii(infojeu):
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

def automatique():
    identifiant, etat = débuter_partie("sttem")
    partie = Quoridor(etat["joueurs"], etat['murs'])
    print(partie)
    while partie.partie_terminée() == False:
        before = copy.deepcopy(partie.état_partie())
        partie.jouer_coup(1)
        after = copy.deepcopy(partie.état_partie())
        print(partie)
        if before["joueurs"][0]["pos"] != after["joueurs"][0]["pos"]:
            etat = jouer_coup(identifiant, "D", after["joueurs"][0]["pos"])
        elif len(after["murs"]["horizontaux"]) != len(before["murs"]["horizontaux"]):
            etat = jouer_coup(identifiant, "MH", after["murs"]["horizontaux"][len(after["murs"]["horizontaux"])-1])
        elif len(after["murs"]["verticaux"]) != len(before["murs"]["verticaux"]):
            etat = jouer_coup(identifiant, "MV", after["murs"]["verticaux"][len(after["murs"]["verticaux"])-1])
        partie = Quoridor(etat["joueurs"], etat['murs'])

if __name__ == "__main__":
    __args__ = analyser_commande()
    if __args__.auto and __args__.graph == False:
        automatique()
    elif __args__.graph and __args__.auto == False:
        print('graphique')
    elif __args__.graph and __args__.auto:
        print('autograph')
    else:
        __infojeutupple__ = débuter_partie(__args__.idul)
        __infojeu1__ = __infojeutupple__[1]
        afficher_damier_ascii(__infojeu1__)
        while True:
            __coup_type__ = input("Choisir un coup: 'D', 'MH' ou 'MV'")
            __position_coup__ = input("veuillez inscrire la position du coup sous format '(x, y)'")
            afficher_damier_ascii(jouer_coup(__infojeutupple__[0], __coup_type__, \
                                  __position_coup__))
