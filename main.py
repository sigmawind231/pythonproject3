"""Module principal du jeu"""
import argparse

from api import débuter_partie, jouer_coup, lister_parties


def analyser_commande():
    """Permet d'utiliser la command line"""
    parser = argparse.ArgumentParser(
        description="Jeu Quoridor - phase 1")
    parser.add_argument(dest='idul', type=str, help="IDUL du joueur.")
    parser.add_argument("-l", "--lister", dest='lister',
                        action="store_true",
                        help="Lister les identifiants de vos 20 dernières parties.")
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

if __name__ == "__main__":
    __args__ = analyser_commande()
    if __args__.lister:
        print(lister_parties(__args__.idul))
    else:
        __infojeutupple__ = débuter_partie(__args__.idul)
        __infojeu1__ = __infojeutupple__[1]
        afficher_damier_ascii(__infojeu1__)
        while True:
            __coup_type__ = input("Choisir un coup: 'D', 'MH' ou 'MV'")
            __position_coup__ = input("veuillez inscrire la position du coup sous format '(x, y)'")
            afficher_damier_ascii(jouer_coup(__infojeutupple__[0], __coup_type__, \
                                  __position_coup__))