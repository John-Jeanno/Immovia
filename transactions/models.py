from django.db import models


class DossierTransaction(models.Model):
    ETAPE_CHOICES = [
        ('initial', 'Initial'),
        ('avant_contrat', 'Avant contrat'),
        ('notaire', 'Notaire'),
        ('cloture', 'Clôturée'),
    ]

    client = models.ForeignKey('clients.Client', null=True, blank=True, on_delete=models.SET_NULL)
    titre = models.CharField(max_length=200, default='')
    etape = models.CharField(max_length=30, choices=ETAPE_CHOICES, default='initial')
    montant = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre or f'Dossier {self.pk}'


class Offre(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('soumise', 'Soumise'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
    ]

    dossier = models.ForeignKey('DossierTransaction', related_name='offres', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Offre {self.pk} - {self.montant}'


class DocumentTransaction(models.Model):
    dossier = models.ForeignKey('DossierTransaction', related_name='documents', on_delete=models.CASCADE)
    nom = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='documents_transactions/', blank=True, null=True)


class HistoriqueNotaire(models.Model):
    dossier = models.ForeignKey('DossierTransaction', related_name='historiques_notaire', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, default='')
