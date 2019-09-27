[Sommaire](https://ursi-2020.github.io/Documentation/)

# API

## Routes

### Get Data
- **URL** : '/api/data'
- **Methods** : ['GET']
- **Query Params** : id (int > 0, Optionnal)
- **Return Value** : JSON [200, 404]
- **Description** : Cette route permet de récupérer les données du catalogue produits:
  - Si *id* n'est pas renseigné, renvoie le catalogue dans son intégralité sous la forme d'une liste JSON
  - Si *id* est renseigné, renvoie les informations du produit correspondant
  - En cas d'erreur, renvoie un code 404 avec un JSON où un champ *error* contiendra un message décrivant l'erreur
