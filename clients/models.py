from django.db import models


class Client(models.Model):
    TYPE_CHOICES = [
        ('ACH', 'Acheteur'),
        ('VEN', 'Vendeur'),
        ('LOC', 'Locataire'),
        ('PRO', 'Propriétaire'),
    ]

    civilite = models.CharField(max_length=10, blank=True, default='')
    nom = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150)
    email = models.EmailField(blank=True, default='')
    telephone = models.CharField(max_length=30, blank=True, default='')
    mobile = models.CharField(max_length=30, blank=True, default='')
    type_client = models.CharField(max_length=10, choices=TYPE_CHOICES, default='ACH')
    budget = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f'{self.prenom} {self.nom}'.strip()


class CritereRecherche(models.Model):
    client = models.ForeignKey('Client', related_name='criteres', on_delete=models.CASCADE)
    type_bien = models.CharField(max_length=30, default='maison')
    ville = models.CharField(max_length=100, blank=True, default='')
    surface_min = models.IntegerField(default=0)
    budget_max = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"Critère de {self.client}"


class Interaction(models.Model):
    client = models.ForeignKey('Client', related_name='interactions', on_delete=models.CASCADE)
    type_interaction = models.CharField(max_length=10, default='TEL')
    date = models.DateTimeField(auto_now_add=True)
    sujet = models.CharField(max_length=200, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    a_relancer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type_interaction} - {self.client}"
