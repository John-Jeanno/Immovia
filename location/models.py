from django.db import models


class Bail(models.Model):
    TYPE_CHOICES = [('vide', 'Vide'), ('meuble', 'Meublé')]

    bien = models.ForeignKey('biens.BienImmobilier', null=True, blank=True, on_delete=models.SET_NULL)
    locataire = models.ForeignKey('clients.Client', null=True, blank=True, on_delete=models.SET_NULL)
    type_bail = models.CharField(max_length=20, choices=TYPE_CHOICES, default='vide')
    loyer_mensuel = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Bail {self.pk}'


class Paiement(models.Model):
    bail = models.ForeignKey('Bail', related_name='paiements', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    date_paiement = models.DateField()
    mode_paiement = models.CharField(max_length=20, default='virement')

    def __str__(self):
        return f'Paiement {self.montant}'


class QuittanceLoyer(models.Model):
    bail = models.ForeignKey('Bail', related_name='quittances', on_delete=models.CASCADE)
    numero = models.CharField(max_length=50, default='')
    date_emission = models.DateField(auto_now_add=True)


class EtatDesLieux(models.Model):
    bail = models.ForeignKey('Bail', related_name='etats_des_lieux', on_delete=models.CASCADE)
    date_etat = models.DateField()
    commentaire = models.TextField(blank=True, default='')


class PhotoEtatLieux(models.Model):
    etat = models.ForeignKey('EtatDesLieux', related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='etat_lieux/', blank=True, null=True)


class Sinistre(models.Model):
    bail = models.ForeignKey('Bail', related_name='sinistres', on_delete=models.CASCADE)
    libelle = models.CharField(max_length=200)
    date_signalement = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, default='')
