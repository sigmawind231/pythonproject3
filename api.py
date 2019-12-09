"""Module d'intéraction avec le serveur du cours"""
import requests

def débuter_partie(idul):
    """ Fonction qui permet de commencer Quoridor"""
    idul = str(idul)
    url_base = 'https://python.gel.ulaval.ca/quoridor/api/'
    rep = requests.post(url_base+'débuter/', data={'idul': idul})
    rep = rep.json()
    if 'message' in rep.keys():
        raise RuntimeError(f"{rep['message']}")
    else:
        return (rep['id'], rep['état'])

def jouer_coup(id_partie, type_coup, position):
    """ Fonction qui permet de joueur un coup sur le jeu"""
    url_base = 'https://python.gel.ulaval.ca/quoridor/api/'
    rep = requests.post(url_base+'jouer/',
                        data={'id': id_partie, 'type': type_coup,
                              'pos': position})
    rep = rep.json()
    if 'message' in rep.keys():
        raise RuntimeError(f"{rep['message']}")
    if 'gagnant' in rep.keys():
        raise StopIteration(f"{rep['gagnant']}")
    else:
        return rep['état']
