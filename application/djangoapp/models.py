from django.db import models

class Produit(models.Model):
    codeProduit = models.CharField(max_length=200, primary_key=True)
    codeProduitFournisseur = models.CharField(max_length=200)
    nomFournisseur = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField()
    packaging = models.PositiveIntegerField()
    prixFournisseur = models.PositiveIntegerField()
    prix = models.PositiveIntegerField()
    exclusivite = models.CharField(max_length=10)

class Log(models.Model):
    date = models.DateTimeField()
    nbCreated = models.PositiveIntegerField(default=0)
    nbDeleted = models.PositiveIntegerField(default=0)
    nbModified = models.PositiveIntegerField(default=0)

class Article(models.Model):
    nom = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return 'Article: {}'.format(self.nom)

class Vente(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return 'Vente: {} - {}'.format(self.article.nom, self.date)

