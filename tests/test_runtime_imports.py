import importlib
import unittest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from biens.models import BienImmobilier


class RuntimeImportsTest(unittest.TestCase):
    def test_location_utils_and_marketing_forms_exist(self):
        location_utils = importlib.import_module('location.utils')
        marketing_forms = importlib.import_module('marketing.forms')

        self.assertTrue(hasattr(location_utils, 'generate_quittance_pdf'))
        self.assertTrue(hasattr(marketing_forms, 'AnnonceFormSet'))

    def test_bien_immobilier_supports_geocoding_fields(self):
        self.assertTrue(hasattr(BienImmobilier, 'geocoder_adresse'))
        field_names = [field.name for field in BienImmobilier._meta.get_fields()]
        self.assertIn('latitude', field_names)
        self.assertIn('longitude', field_names)


class MapViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='maptester', password='secret123')
        self.user.user_permissions.add(Permission.objects.get(codename='view_bienimmobilier'))

    def test_liste_biens_exposes_map_properties(self):
        BienImmobilier.objects.create(
            titre='Villa test',
            description='Maison de test',
            prix=1500000,
            surface=120,
            nombre_pieces=4,
            type_bien='maison',
            statut='disponible',
            adresse='Plateau',
            ville='Dakar',
            code_postal='18200',
            latitude=14.676817,
            longitude=-17.439291,
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse('biens:liste_biens'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('map_properties', response.context)
        self.assertGreater(len(response.context['map_properties']), 0)
        self.assertContains(response, 'id="property-map"')


if __name__ == '__main__':
    unittest.main()
