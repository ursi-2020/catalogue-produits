# Generated by Django 2.2.5 on 2019-09-20 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0003_produit_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produit',
            old_name='nom',
            new_name='code_produit',
        ),
        migrations.RenameField(
            model_name='produit',
            old_name='nom_fournisseur',
            new_name='description_produit',
        ),
        migrations.RenameField(
            model_name='produit',
            old_name='id_fournisseur',
            new_name='packaging',
        ),
        migrations.RemoveField(
            model_name='produit',
            name='prix_achat',
        ),
        migrations.AddField(
            model_name='produit',
            name='famille_produit',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='prix',
            field=models.PositiveIntegerField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='produit',
            name='quantite_min',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]