import argparse

infojeu= {
    "joueurs": [
        {"nom": "idul", "murs": 7, "pos": [5, 5]}, 
        {"nom": "automate", "murs": 3, "pos": [8, 6]}
    ], 
    "murs": {
        "horizontaux": [[4, 4], [2, 6], [3, 8], [5, 8], [7, 8]], 
        "verticaux": [[6, 2], [4, 4], [2, 6], [7, 5], [7, 7]]
    }
}

def main(args):
    print(args)

def analyser_commande():
    parser = argparse.ArgumentParser(
        description = "Enregistre le nom du joueur"
    )
    parser.add_argument(dest='idul', type=str)
    args = parser.parse_args()
    return args

def afficher_damier_ascii(infojeu):
    lignes = []
    lignes += list("Légende: 1="+ str(infojeu["joueurs"][0]["nom"])+', 2='+str(infojeu["joueurs"][1]["nom"]) + "\n")
    lignes += list("   "+"-"*35+"\n")
    for i in range(1,10):
        lignes += str(10-i) + " | "
        for j in range (1,9):
            strplayer = "."
            if [j, 10-i] == infojeu["joueurs"][0]["pos"]:
                strplayer = "1"
            elif [j, 10-i] == infojeu["joueurs"][1]["pos"]:
                strplayer = "2"
            if [j+1,10-i] in infojeu["murs"]["verticaux"]:
                lignes += list(strplayer + " | ")
            elif [j+1,9-i] in infojeu["murs"]["verticaux"]:
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
        for k in range (1,9):
            if i != 9:
                if [k,10-i] in infojeu["murs"]["horizontaux"]:
                    lignes += list("----")
                elif [k-1,10-i] in infojeu["murs"]["horizontaux"] and [k+1,9-i] in infojeu["murs"]["verticaux"]:
                    lignes += list("---|")
                elif [k-1,10-i] in infojeu["murs"]["horizontaux"]:
                    lignes += list("--- ")
                elif [k+1,9-i] in infojeu["murs"]["verticaux"]:
                    lignes += list("   |")
                else:
                    lignes += list("    ")
        if i != 9:
            if [8,10-i] in infojeu["murs"]["horizontaux"]:
                    lignes += list("---|")
            else: 
                lignes += list("   |")
        lignes += list("\n")          
    lignes += list("--|"+ "-"*35+"\n")
    lignes += list("  | 1   2   3   4   5   6   7   8   9")
    lignes = ''.join(lignes)
    print(lignes)

if __name__ == "__main__":
    args = analyser_commande()
    afficher_damier_ascii(infojeu)
