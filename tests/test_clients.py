from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from clients.models import Client


class ClientCreateViewTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(username='clienttester', password='secret123')
        self.client.force_login(user)

    def test_valid_post_creates_client_and_redirects_to_list(self):
        response = self.client.post(reverse('clients:create'), {
            'civilite': 'M.',
            'nom': 'Dupont',
            'prenom': 'Alice',
            'email': 'alice@example.com',
            'telephone': '0123456789',
            'mobile': '',
            'type_client': 'ACH',
            'budget': '250000.00',
            'notes': 'Recherche une maison.',
        })

        self.assertRedirects(response, reverse('clients:list'))
        self.assertTrue(Client.objects.filter(nom='Dupont', prenom='Alice').exists())

    def test_invalid_post_keeps_form_and_does_not_create_client(self):
        response = self.client.post(reverse('clients:create'), {'prenom': 'Alice'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ce champ est obligatoire.')
        self.assertEqual(Client.objects.count(), 0)