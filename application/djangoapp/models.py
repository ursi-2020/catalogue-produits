from django.db import models

class Produit(models.Model):
    nom = models.CharField(max_length=200)
    id_fournisseur = models.PositiveIntegerField()
    nom_fournisseur = models.CharField(max_length=200)
    prix_achat = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return 'Produit: {}'.format(self.nom)