import logging

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class BienImmobilier(models.Model):
    TYPE_BIEN = [
        ('maison', 'Maison'),
        ('appartement', 'Appartement'),
        ('terrain', 'Terrain'),
    ]
    STATUT_CHOIX = [
        ('disponible', 'Disponible'),
        ('reserve', 'Réservé'),
        ('vendu_loue', 'Vendu/Loué'),
        ('negociation', 'En négociation'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    prix = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    surface = models.IntegerField(default=0)
    nombre_pieces = models.IntegerField(default=0)
    type_bien = models.CharField(max_length=20, choices=TYPE_BIEN, default='maison')
    statut = models.CharField(max_length=20, choices=STATUT_CHOIX, default='disponible')
    adresse = models.CharField(max_length=200, blank=True, default='')
    ville = models.CharField(max_length=100, blank=True, default='')
    code_postal = models.CharField(max_length=20, blank=True, default='')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre

    def geocoder_adresse(self):
        """Utilise l'API Nominatim pour calculer latitude/longitude à partir de l'adresse."""
        if not self.adresse or not self.ville:
            return False

        try:
            from geopy.geocoders import Nominatim
            from geopy.exc import GeocoderTimedOut, GeocoderServiceError
        except Exception:
            logger.warning('geopy non disponible, géocodage ignoré.')
            return False

        query = ', '.join(part for part in [self.adresse, self.code_postal, self.ville, 'Sénégal'] if part)
        try:
            geolocator = Nominatim(user_agent='immovia-geocoder')
            location = geolocator.geocode(query, timeout=10)
            if location:
                self.latitude = location.latitude
                self.longitude = location.longitude
                logger.info('Géocodage réussi pour %s -> %s, %s', query, self.latitude, self.longitude)
                return True
            logger.warning('Adresse non trouvée pour %s', query)
            return False
        except (GeocoderTimedOut, GeocoderServiceError, ValueError) as exc:
            logger.warning('Erreur de géocodage: %s', exc)
            return False

    def save(self, *args, **kwargs):
        if (not self.latitude or not self.longitude) and self.adresse and self.ville:
            self.geocoder_adresse()
        super().save(*args, **kwargs)


class ImageBien(models.Model):
    bien = models.ForeignKey('BienImmobilier', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images_biens/', blank=True, null=True)
    legende = models.CharField(max_length=200, blank=True, default='')


class Mandat(models.Model):
    bien = models.OneToOneField('BienImmobilier', on_delete=models.CASCADE)
    type_mandat = models.CharField(max_length=20, default='simple')
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    actif = models.BooleanField(default=True)
