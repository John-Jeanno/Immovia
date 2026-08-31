from django.db import models


class Chantier(models.Model):
    ETAT_CHOICES = [
        ('planifie', 'Planifié'),
        ('preparation', 'Préparation'),
        ('en_cours', 'En cours'),
        ('finition', 'Finition'),
        ('termine', 'Terminé'),
        ('livre', 'Livré'),
        ('en_retard', 'En retard'),
    ]

    nom = models.CharField(max_length=200)
    adresse = models.CharField(max_length=200, blank=True, default='')
    budget = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    budget_depense = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    pourcentage_avancement = models.IntegerField(default=0)
    etat_chantier = models.CharField(max_length=20, choices=ETAT_CHOICES, default='planifie')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
