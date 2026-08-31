from django.db import models


class CompteBancaire(models.Model):
    TYPE_CHOICES = [('courant', 'Courant'), ('epargne', 'Epargne')]
    nom = models.CharField(max_length=200)
    numero = models.CharField(max_length=100, blank=True, default='')
    banque = models.CharField(max_length=200, blank=True, default='')
    type_compte = models.CharField(max_length=20, choices=TYPE_CHOICES, default='courant')
    solde_initial = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    date_ouverture = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom


class Categorie(models.Model):
    TYPE_CHOICES = [('recette', 'Recette'), ('depense', 'Dépense')]
    nom = models.CharField(max_length=200)
    type_categorie = models.CharField(max_length=20, choices=TYPE_CHOICES, default='depense')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.nom


class Facture(models.Model):
    TYPE_CHOICES = [('honoraire', 'Honoraires'), ('frais_agence', 'Frais agence'), ('autre', 'Autre')]
    STATUT_CHOICES = [('brouillon', 'Brouillon'), ('emise', 'Émise'), ('payee', 'Payée')]

    numero = models.CharField(max_length=50, default='FAC-0001')
    type_facture = models.CharField(max_length=30, choices=TYPE_CHOICES, default='honoraire')
    client = models.ForeignKey('clients.Client', null=True, blank=True, on_delete=models.SET_NULL)
    date_emission = models.DateField(null=True, blank=True)
    date_echeance = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    montant_ht = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    tva = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    montant_ttc = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return self.numero


class Operation(models.Model):
    compte = models.ForeignKey('CompteBancaire', null=True, blank=True, on_delete=models.SET_NULL)
    categorie = models.ForeignKey('Categorie', null=True, blank=True, on_delete=models.SET_NULL)
    montant = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    date_operation = models.DateField(null=True, blank=True)
    date_valeur = models.DateField(null=True, blank=True)
    mode_paiement = models.CharField(max_length=30, default='virement')
    libelle = models.CharField(max_length=200, default='')
    facture = models.ForeignKey('Facture', null=True, blank=True, related_name='operations', on_delete=models.SET_NULL)

    def __str__(self):
        return self.libelle or f'Opération {self.pk}'
