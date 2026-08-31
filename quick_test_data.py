#!/usr/bin/env python
"""
Script rapide pour créer des données de test sénégalaises
"""
import sys
import os

# Ajouter le répertoire immovia au chemin
sys.path.insert(0, '/Users/john/immo/immovia')

# Désactiver celery avant d'importer Django
os.environ['CELERY_TASK_ALWAYS_EAGER'] = 'true'
os.environ['CELERY_BROKER_URL'] = 'memory://'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from django.contrib.auth.models import User
from biens.models import BienImmobilier, Mandat
from clients.models import Client
from location.models import Bail, Paiement
from datetime import date, timedelta
import random

print("Création des données sénégalaises...")

# Données sénégalaises
PRENOMS = ['Moussa', 'Fatou', 'Omar', 'Aïssatou', 'Amadou', 'Papa', 'Seydou', 'Khady', 'Mamadou', 'Awa']
NOMS = ['Diop', 'Sy', 'Ba', 'Sow', 'Gueye', 'Fall', 'Ndiaye', 'Kane', 'Sane', 'Coulibaly']
VILLES = ['Dakar', 'Saint-Louis', 'Kaolack', 'Thiès', 'Tambacounda', 'Kolda', 'Ziguinchor']

# Créer admin
User.objects.filter(username='admin').delete()
admin = User.objects.create_superuser('admin', 'admin@immovia.sn', 'admin123')
print(f"✅ Administrateur créé: admin / admin123")

# Créer 10 biens
BIENS_DATA = [
    ('Villa avec piscine - Ngor', 'Ngor', 350, 5, 350000000),
    ('Appartement moderne - Plateau', 'Plateau', 120, 3, 85000000),
    ('Terrain 500m² - Thiès', 'Centre-ville', 500, 0, 25000000),
    ('Magasin commercial - Parcelles', 'Parcelles-Assainies', 80, 2, 45000000),
    ('Maison 4 pièces - Hann', 'Hann', 180, 4, 120000000),
    ('Petit immeuble R+2 - Yoff', 'Yoff', 250, 6, 180000000),
    ('Studio meublé - Medina', 'Medina', 35, 1, 12000000),
    ('Terrain + maison inachevée - Kaolack', 'Kaolack', 800, 3, 35000000),
    ('Duplex haut standing - Almadies', 'Almadies', 280, 6, 450000000),
    ('Lot terrain 1000m² - Tambacounda', 'Tambacounda', 1000, 0, 15000000),
]

biens = []
for titre, adresse, surface, pieces, prix in BIENS_DATA:
    bien = BienImmobilier.objects.create(
        titre=titre,
        description=f"Bien immobilier à {adresse}, Sénégal",
        prix=prix,
        surface=surface,
        nombre_pieces=pieces,
        type_bien='maison' if pieces > 0 else 'terrain',
        statut='disponible',
        adresse=adresse,
        ville=random.choice(VILLES),
        code_postal='00221'
    )
    biens.append(bien)
    Mandat.objects.create(
        bien=bien,
        type_mandat=random.choice(['exclusif', 'simple']),
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=365),
        actif=True
    )

print(f"✅ {len(biens)} biens créés")

# Créer 15 clients
clients = []
for i in range(15):
    # Utiliser des emails uniques
    email = f"client_{i}_{random.randint(1000,9999)}@immovia.sn"
    
    # Vérifier si le client existe déjà
    if not Client.objects.filter(email=email).exists():
        client = Client.objects.create(
            civilite=random.choice(['M', 'Mme']),
            nom=random.choice(NOMS),
            prenom=random.choice(PRENOMS),
            email=email,
            telephone=f"+221{random.randint(33000000, 39999999)}",
            mobile=f"+221{random.randint(70000000, 79999999)}",
            type_client=random.choice(['ACH', 'VEN', 'LOC']),
            budget=random.randint(10000000, 500000000),
            notes="Client sénégalais"
        )
        clients.append(client)

print(f"✅ {len(clients)} clients créés")

# Créer 4 baux
for bien in biens[:4]:
    client = random.choice(clients)
    bail = Bail.objects.create(
        bien=bien,
        locataire=client,
        date_debut=date.today() - timedelta(days=90),
        date_fin=date.today() + timedelta(days=275),
        type_bail='meuble' if bien.nombre_pieces <= 2 else 'vide',
        loyer_mensuel=random.randint(5000000, 50000000),
        charges_mensuelles=random.randint(500000, 2000000),
        depot_garantie=random.randint(5000000, 50000000),
        renouvellement_auto=True,
        actif=True
    )
    Paiement.objects.create(
        bail=bail,
        montant=bail.loyer_mensuel,
        date_paiement=date.today(),
        periode_couverte="Janvier 2026",
        mode_paiement="virement",
        reference=f"VIR{bail.id:04d}"
    )

print(f"✅ 4 baux de location créés")

print("\n" + "="*60)
print("✅ APPLICATION ADAPTÉE POUR LE SÉNÉGAL!")
print("="*60)
print("✓ 10 biens immobiliers sénégalais")
print("✓ 15 clients sénégalais")
print("✓ 4 baux de location")
print("✓ Devises en FCFA")
print("✓ Villes du Sénégal")
print("="*60)
print("\nConnexion admin:")
print("  Identifiant: admin")
print("  Mot de passe: admin123")
print("="*60)

