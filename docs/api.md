[Sommaire](https://ursi-2020.github.io/catalogue-produits/)

# JSON API

## Applications
### Get all products

Get the products registered in the catalogue produits db.

If a familleProduit is specified, returns only the products that match this category of products.

**Service name** : `catalogue-produit`

**URL** : `api/get-all`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : familleProduit : *string*

**Content examples:**


```json
{
  "produits": [
    {
      "codeProduit": "fo-X1-1",
      "codeProduitFournisseur": "X1-1",
      "nomFournisseur": "fo",
      "familleProduit": "Console",
      "descriptionProduit": "Console:P3-1",
      "quantiteMin": 5,
      "packaging": 1,
      "prixFournisseur" : 180,
      "prix": 200,
      "exclusivite": ""
    },
    {
      "codeProduit": "fo-X1-0",
      "codeProduitFournisseur": "X1-1",
      "nomFournisseur": "fo",
      "familleProduit": "Frigos",
      "descriptionProduit": "Frigos:P1-0",
      "quantiteMin": 15,
      "packaging": 2,
      "prixFournisseur" : 180,
      "prix": 200,
      "exclusivite": "ecommerce"
    },
  ]
}
```

### Get ecommerce products

Get the products that ecommerce can sell registered in the catalogue produits db.

If a familleProduit is specified, returns only the products that match this category of products.

**Service name** : `catalogue-produit`

**URL** : `api/get-ecommerce`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : familleProduit : *string*

**Content examples:**


```json
{
  "produits": [
    {
      "codeProduit": "fo-X1-0",
      "codeProduitFournisseur": "X1-1",
      "nomFournisseur": "fo",
      "familleProduit": "Frigos",
      "descriptionProduit": "Frigos:P1-0",
      "quantiteMin": 15,
      "packaging": 2,
      "prixFournisseur": 180,
      "prix": 200,
      "exclusivite": "ecommerce"
    },
    {
      "codeProduit": "fo-X1-1",
      "codeProduitFournisseur": "X1-1",
      "nomFournisseur": "fo",
      "familleProduit": "Console",
      "descriptionProduit": "Console:P3-1",
      "quantiteMin": 5, "packaging": 1,
      "prixFournisseur" : 180,
      "prix": 200,
      "exclusivite": ""
    }
  ]
}
```

### Get magasin products

Get the products that magasin can sell registered in the Catalogue Produit db.

If a familleProduit is specified, returns only the products that match this category of products.

**Service name** : `catalogue-produit`

**URL** : `api/get-magasin`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : familleProduit : *string*

**Content examples:**


```json
{
  "produits": [
    {
      "codeProduit": "fo-X1-1",
      "codeProduitFournisseur": "X1-1",
      "nomFournisseur": "fo",
      "familleProduit": "Console",
      "descriptionProduit": "Console:P3-1",
      "quantiteMin": 5,
      "packaging": 1,
      "prixFournisseur" : 180,
      "prix": 200,
      "exclusivite": ""
    },
    {
      "codeProduit": "fo-X1-2",
      "codeProduitFournisseur": "X1-1",
      "nomFournisseur": "fo",
      "familleProduit": "Frigos",
      "descriptionProduit": "Frigos:P3-2",
      "quantiteMin": 10,
      "packaging": 1,
      "prixFournisseur" : 180,
      "prix": 200,
      "exclusivite": "magasin"}
  ]
}
```

### Get one product by id

Get the details of a product registered in the Catalogue Produit db with ID.

**Service name** : `catalogue-produit`

**URL** : `api/get-by-id/<id>`

**Method** : `GET`

**Auth required** : NO

**Content examples:**

*Success*
```json
{
  "produit" : {
    "codeProduit": "fo-X1-1",
    "codeProduitFournisseur": "X1-1",
    "nomFournisseur": "fo",
    "familleProduit": "Console",
    "descriptionProduit": "Console:P3-1",
    "quantiteMin": 5,
    "packaging": 1,
    "prixFournisseur" : 180,
    "prix": 200,
    "exclusivite": ""
  }
}
```

*Error*
```json
{
  "error": "ID produit invalide ou produit inexistant"
}
```

### Get products with Drive (File Manager)

Formulate a request to receive the catalogue by file manager. This file will contain the products registered in the catalogue produits db.
Depending on the app calling this route, the file will not contain the same products (ecommerce and magasin have their exclusivity).

**Service name** : `catalogue-produit`

**URL** : `api/file/products`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : app : *string* MANDATORY

**Content examples:**

Success
```json
{
  "info": "File successfully append to the sending queue"
}
```

Error if no app provided
```json
{
  "error": "Veuillez specifier votre nom d'application"
}
```

Error if app is not registered
```json
{
  "error": "App doesn't exist or did not register in our drive"
}
```

## Simulateur
The following routes are designed to be called by the simulator

### Get all ecommerce products

Get all the products registered in the catalogue db that ecommerce can sold.

**Service name** : `catalogue-produit`

**URL** : `api/simulateur/get-all-ecommerce`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : N/A

**Content examples:**

Success

```json
{
    "produits": [
        {
            "codeProduit": "fo-X1-0",
            "codeProduitFournisseur": "X1-0",
            "nomFournisseur": "fo"
        },
        {
            "codeProduit": "fo-X1-1",
            "codeProduitFournisseur": "X1-1",
            "nomFournisseur": "fo"
        },
        {
            "codeProduit": "fo-X1-2",
            "codeProduitFournisseur": "X1-2",
            "nomFournisseur": "fo"
        },
        {
            "codeProduit": "fo-X1-3",
            "codeProduitFournisseur": "X1-3",
            "nomFournisseur": "fo"
        }
    ]
}
```
### Get by code

Get a product registered in the catalogue db that matches the nomFournisseur and the codeProduitFournisseur given as parameters.

If those parameters are not present, returns an error.

*NB: If the exclusivite field is empty, this product is available at both magasin and ecommerce*

**Service name** : `catalogue-produit`

**URL** : `api/simulateur/get-by-code`

**Method** : `GET`

**Auth required** : NO

**Query Parameters** : 
- nomFournisseur : *string* **MANDATORY**
- codeProduitFournisseur : *string* **MANDATORY**

**Content examples:**

Success

```json
{
    "produit": {
        "codeProduit": "fo-X1-1",
        "codeProduitFournisseur": "X1-1",
        "nomFournisseur": "fo",
        "exclusivite": ""
    }
}
```

Errors
```json
{
    "error": "Produit inexistant"
}
```

```json
{
    "error": "Missing codeProduitFournisseur in query parameter"
}
```

```json
{
    "error": "Missing nomFournisseur in query parameter"
}
```