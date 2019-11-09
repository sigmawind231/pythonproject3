import requests

url = 'http://www.ulaval.ca/'

rep = requests.get(url)

if rep.status_code == 200:
    # la réponse est bonne, afficher son contenu
    print(rep.text)
    
else:
    # afficher un message d'erreur
    print(f"Le GET sur {url} a produit le code d'erreur {rep.status_code}.")