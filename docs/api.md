[Sommaire](https://ursi-2020.github.io/Documentation/)

# API

## Routes

### Get Data
- **URL** : 'catalogueproduit/api/data'
- **Methods** : ['GET']
- **Query Params** : id (int > 0, optionnal)
- **Return Value** : JSON [200, 404]
- **Description** : Cette route permet de récupérer les données du catalogue produits:
  - Si *id* est renseigné, renvoie le produit associé à cet id
  - Sinon, renvoie l'intégralité du catalogue produit sous forme d'une liste JSON
  - En cas d'erreur, renvoie un code 404 avec un JSON où un champ *error* contiendra un message décrivant l'erreur
