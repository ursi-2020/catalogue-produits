from django.db import models

class Produit(models.Model):
    codeProduit = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField()
    packaging = models.PositiveIntegerField()
    prix = models.PositiveIntegerField()

    def __str__(self):
        return 'Produit: {}'.format(self.nom)


class User(models.Model):
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    age = models.PositiveIntegerField()

    def __str__(self):
        return 'User: {}'.format(self.nom)

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