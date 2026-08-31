from django.db import models


class CreneauDisponible(models.Model):
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    lieu = models.CharField(max_length=200, blank=True, default='')
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.date_debut} - {self.date_fin}'


class RendezVous(models.Model):
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('effectue', 'Effectué'),
        ('annule', 'Annulé'),
    ]

    creneau = models.ForeignKey('CreneauDisponible', related_name='rendez_vous', on_delete=models.CASCADE)
    client = models.ForeignKey('clients.Client', null=True, blank=True, on_delete=models.SET_NULL)
    objet = models.CharField(max_length=200, default='Visite')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    notes = models.TextField(blank=True, default='')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.objet} - {self.statut}'


class RapportVisite(models.Model):
    rendez_vous = models.ForeignKey('RendezVous', related_name='rapports', on_delete=models.CASCADE)
    present = models.BooleanField(default=True)
    commentaire = models.TextField(blank=True, default='')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rapport - {self.rendez_vous.id}'
