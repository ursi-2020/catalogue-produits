#catalogue produit

We have create the entity which contain the all informations of all the products.

All product have 5 informations : 
	    
            "codeProduit": "X1-0",
            "familleProduit": "Frigos",
            "descriptionProduit": "Frigos:P1-0",
            "quantiteMin": 15,
            "packaging": 2,
            "prix": 4.24

The other application can ask us all infomations by the following WebService : https://catalogueproduit/api/data

Or the can ask us informations for only one product with his id with this WebService : https://catalogueproduit/api/data?id=1

All the informations will send in a Json file.
If the product doesn't exist, you will receive 404 error.
