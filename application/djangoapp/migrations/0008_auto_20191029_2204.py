# Generated by Django 2.2.6 on 2019-10-29 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoapp', '0007_produit_exclusivite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='id',
        ),
        migrations.AlterField(
            model_name='produit',
            name='codeProduit',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
