# Generated by Django 2.2.5 on 2019-09-20 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0004_auto_20190920_0934'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produit',
            old_name='code_produit',
            new_name='codeProduit',
        ),
        migrations.RenameField(
            model_name='produit',
            old_name='description_produit',
            new_name='descriptionProduit',
        ),
        migrations.RenameField(
            model_name='produit',
            old_name='famille_produit',
            new_name='familleProduit',
        ),
        migrations.RenameField(
            model_name='produit',
            old_name='quantite_min',
            new_name='quantiteMin',
        ),
    ]
