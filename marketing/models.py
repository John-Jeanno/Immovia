from django.db import models


class CampagneMarketing(models.Model):
    nom = models.CharField(max_length=200)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom


class Annonce(models.Model):
    campagne = models.ForeignKey('CampagneMarketing', related_name='annonces', on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')


class EmailMarketing(models.Model):
    campagne = models.ForeignKey('CampagneMarketing', related_name='emails', on_delete=models.CASCADE)
    sujet = models.CharField(max_length=200)
    corps = models.TextField(blank=True, default='')


class DestinataireEmail(models.Model):
    email = models.EmailField()
    campagne = models.ForeignKey('CampagneMarketing', related_name='destinataires', on_delete=models.CASCADE)


class PublicationSociale(models.Model):
    campagne = models.ForeignKey('CampagneMarketing', related_name='publications', on_delete=models.CASCADE)
    contenu = models.TextField()


class SiteVitrine(models.Model):
    nom = models.CharField(max_length=200)
    url = models.URLField()
