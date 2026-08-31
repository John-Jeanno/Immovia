import os
import django
from django.conf import settings

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from django.contrib.auth.models import User
from biens.models import BienImmobilier, ImageBien, Mandat
from clients.models import Client, CritereRecherche, Interaction
from comptabilite.models import CompteBancaire, Categorie, Facture, Operation
from location.models import Bail, Paiement, QuittanceLoyer, EtatDesLieux, PhotoEtatLieux, Sinistre
from marketing.models import CampagneMarketing, Annonce, EmailMarketing, DestinataireEmail, PublicationSociale, SiteVitrine
from rendezvous.models import CreneauDisponible, RendezVous, RapportVisite, PhotoVisite
from transactions.models import DossierTransaction, Offre, DocumentTransaction, HistoriqueNotaire
from datetime import date, timedelta
import random
from django.utils import timezone
import uuid

# Créer un utilisateur admin si nécessaire
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')

user = User.objects.get(username='admin')

# Données sénégalaises
PRENOMS_SENEGALAIS = ['Moussa', 'Fatou', 'Omar', 'Aïssatou', 'Amadou', 'Marème', 'Seydou', 'Yacine', 
                       'Papa', 'Khady', 'Mamadou', 'Awa', 'Ibrahima', 'Ndeye', 'Sitor', 'Coumba',
                       'Baidy', 'Assatou', 'Ousmane', 'Astou', 'Demba', 'Aby', 'Lamine', 'Maimouna']

NOMS_SENEGALAIS = ['Diop', 'Sy', 'Ba', 'Sow', 'Gueye', 'Fall', 'Ndiaye', 'Sane', 'Sarr', 'Kane',
                    'Dia', 'Seck', 'Ndoye', 'Samb', 'Coulibaly', 'Traore', 'Camara', 'Bah', 'Keita', 'Beye']

VILLES_SENEGAL = ['Dakar', 'Saint-Louis', 'Kaolack', 'Thiès', 'Tambacounda', 'Louga', 'Kolda', 'Ziguinchor', 'Matam', 'Kédougou']

QUARTIERS_DAKAR = ['Plateau', 'Medina', 'Fann', 'Sicap', 'Parcelles-Assainies', 'Yoff', 'Ouakam', 
                    'Grand-Yoff', 'Almadies', 'HLM', 'Liberté', 'Hann', 'Ngor', 'Sacré-Cœur']

TYPE_BIENS_SEN = [
    ('maison', 'Villa'),
    ('appartement', 'Appartement'),
    ('terrain', 'Terrain'),
    ('magasin', 'Magasin'),
    ('local', 'Local commercial')
]

# Biens immobiliers sénégalais
biens = []
bien_data = [
    {
        'titre': 'Villa avec piscine - Ngor',
        'surface': 350,
        'pieces': 5,
        'prix': 350000000,
        'type': 'maison',
        'quartier': 'Ngor',
        'desc': 'Magnifique villa avec piscine, jardin aménagé, électricité et eau courante, quartier résidentiel sécurisé'
    },
    {
        'titre': 'Appartement moderne - Plateau',
        'surface': 120,
        'pieces': 3,
        'prix': 85000000,
        'type': 'appartement',
        'quartier': 'Plateau',
        'desc': 'Appartement spacieux dans immeuble de standing, ascenseur, accès aisé aux services'
    },
    {
        'titre': 'Terrain 500m² - Thies',
        'surface': 500,
        'pieces': 0,
        'prix': 25000000,
        'type': 'terrain',
        'quartier': 'Centre-ville',
        'desc': 'Beau terrain bien situé, viabilisé, idéal pour construction résidentielle'
    },
    {
        'titre': 'Magasin commercial - Parcelles',
        'surface': 80,
        'pieces': 2,
        'prix': 45000000,
        'type': 'magasin',
        'quartier': 'Parcelles-Assainies',
        'desc': 'Local commercial bien situé, beaucoup de passage, idéal pour commerce'
    },
    {
        'titre': 'Maison 4 pièces - Hann',
        'surface': 180,
        'pieces': 4,
        'prix': 120000000,
        'type': 'maison',
        'quartier': 'Hann',
        'desc': 'Maison solide, bien entretenue, garage, grande cour, quartier calme'
    },
    {
        'titre': 'Petit immeuble R+2 - Yoff',
        'surface': 250,
        'pieces': 6,
        'prix': 180000000,
        'type': 'maison',
        'quartier': 'Yoff',
        'desc': 'Petit immeuble de 3 étages, 2 appartements par étage, bon rendement locatif'
    },
    {
        'titre': 'Studio meublé - Medina',
        'surface': 35,
        'pieces': 1,
        'prix': 12000000,
        'type': 'appartement',
        'quartier': 'Medina',
        'desc': 'Studio mignon et fonctionnel, meublé, proche des transports'
    },
    {
        'titre': 'Terrain + maison inachevée - Kaolack',
        'surface': 800,
        'pieces': 3,
        'prix': 35000000,
        'type': 'terrain',
        'quartier': 'Kaolack',
        'desc': 'Terrain ample avec structure de maison en cours, à finir selon vos plans'
    },
    {
        'titre': 'Duplex haut standing - Almadies',
        'surface': 280,
        'pieces': 6,
        'prix': 450000000,
        'type': 'maison',
        'quartier': 'Almadies',
        'desc': 'Duplex luxueux, salle de bain, cuisine équipée, vue sur mer proche'
    },
    {
        'titre': 'Lot terrain 1000m² - Tambacounda',
        'surface': 1000,
        'pieces': 0,
        'prix': 15000000,
        'type': 'terrain',
        'quartier': 'Tambacounda',
        'desc': 'Grand terrain disponible dans zone en développement, bon investissement'
    }
]

for data in bien_data:
    bien = BienImmobilier.objects.create(
        titre=data['titre'],
        description=data['desc'],
        prix=data['prix'],
        surface=data['surface'],
        nombre_pieces=data['pieces'],
        type_bien=data['type'],
        statut='disponible',
        adresse=data['quartier'],
        ville=random.choice(VILLES_SENEGAL),
        code_postal='00221'  # Code Sénégal
    )
    biens.append(bien)

    # Mandat
    Mandat.objects.create(
        bien=bien,
        type_mandat=random.choice(['exclusif', 'simple']),
        date_debut=date.today(),
        date_fin=date.today() + timedelta(days=365),
        actif=True
    )

print(f"✅ {len(biens)} biens créés")

# Clients sénégalais
clients = []
for i in range(15):
    prenom = random.choice(PRENOMS_SENEGALAIS)
    nom = random.choice(NOMS_SENEGALAIS)
    
    client = Client.objects.create(
        civilite=random.choice(['M', 'Mme']),
        nom=nom,
        prenom=prenom,
        email=f"{prenom.lower()}.{nom.lower()}@example.sn",
        telephone=f"+221{random.randint(30000000, 39999999)}",
        mobile=f"+221{random.randint(70000000, 79999999)}",
        type_client=random.choice(['ACH', 'VEN', 'LOC', 'PRO']),
        budget=random.randint(10000000, 500000000) if random.choice([True, False]) else None,
        notes="Client sénégalais"
    )
    clients.append(client)

    # Critères de recherche
    if random.choice([True, False]):
        CritereRecherche.objects.create(
            client=client,
            type_bien=random.choice(list(zip(*TYPE_BIENS_SEN))[0]),
            ville=random.choice(VILLES_SENEGAL),
            surface_min=random.randint(50, 150),
            budget_max=random.randint(50000000, 300000000)
        )

    # Interaction
    Interaction.objects.create(
        client=client,
        type_interaction=random.choice(['TEL', 'MAIL', 'VIS', 'RDV']),
        date=timezone.now(),
        sujet="Recherche de bien immobilier",
        notes="Client intéressé par l'immobilier au Sénégal",
        a_relancer=random.choice([True, False])
    )

print(f"✅ {len(clients)} clients créés")

# Comptabilite
compte = CompteBancaire.objects.create(
    nom="Compte SGBS Dakar",
    numero="SG1234567890",
    banque="Société Générale Sénégal",
    type_compte="courant",
    solde_initial=500000000,
    date_ouverture=date.today(),
    actif=True
)

print("✅ Compte bancaire créé")


categories = []
for nom in ['Loyers', 'Commissions', 'Frais de dossier', 'Dépenses opérationnelles', 'Utilities']:
    categorie = Categorie.objects.create(
        nom=nom,
        type_categorie='recette' if nom in ['Loyers', 'Commissions'] else 'depense',
        description=f"Catégorie {nom}"
    )
    categories.append(categorie)

print(f"✅ {len(categories)} catégories créées")

# Factures
for i in range(8):
    facture = Facture.objects.create(
        type_facture=random.choice(['honoraire', 'frais_agence', 'autre']),
        client=random.choice(clients),
        date_emission=date.today(),
        date_echeance=date.today() + timedelta(days=30),
        statut=random.choice(['brouillon', 'emise', 'payee']),
        montant_ht=random.randint(5000000, 25000000),
        tva=random.randint(500000, 5000000),
        montant_ttc=random.randint(5500000, 30000000)
    )

    Operation.objects.create(
        compte=compte,
        categorie=random.choice(categories),
        montant=facture.montant_ttc,
        date_operation=date.today(),
        date_valeur=date.today(),
        mode_paiement=random.choice(['carte', 'virement', 'cheque', 'especes']),
        libelle=f"Facture n°{facture.numero}",
        facture=facture
    )

print(f"✅ {len(list(Facture.objects.all()))} factures créées")

# Location - Baux sénégalais
for i in range(4):
    bail = Bail.objects.create(
        bien=random.choice(biens),
        locataire=random.choice(clients),
        date_debut=date.today() - timedelta(days=90),
        date_fin=date.today() + timedelta(days=275),
        type_bail=random.choice(['vide', 'meuble']),
        loyer_mensuel=random.randint(5000000, 50000000),  # En FCFA
        charges_mensuelles=random.randint(500000, 2000000),
        depot_garantie=random.randint(5000000, 50000000),
        clauses_speciales="Paiement avant le 5 de chaque mois",
        renouvellement_auto=True,
        actif=True
    )

    # Paiements mensuels
    for mois in range(-2, 1):
        Paiement.objects.create(
            bail=bail,
            montant=bail.loyer_mensuel,
            date_paiement=date.today() + timedelta(days=mois*30),
            periode_couverte=f"Mois {mois}",
            mode_paiement=random.choice(['virement', 'especes']),
            reference=f"VIR{i}{mois}"
        )

    # États des lieux
    EtatDesLieux.objects.create(
        bail=bail,
        type_etat='entree',
        date_etat=bail.date_debut,
        remarques="Bien en bon état à l'entrée",
        signe_proprietaire=True,
        signe_locataire=True
    )

print(f"✅ {len(list(Bail.objects.all()))} baux créés")

# Marketing sénégalais
campagne = CampagneMarketing.objects.create(
    nom="Campagne Immobilier Dakar 2026",
    type_campagne=random.choice(['email', 'reseaux', 'portail']),
    date_lancement=timezone.now(),
    cible="Investisseurs et clients cherchant bien immobilier au Sénégal",
    statut="active",
    budget=50000000
)

print(f"✅ Campagne marketing créée")

for bien in biens[:6]:
    Annonce.objects.create(
        bien=bien,
        porteurs=random.choice(['leboncoin', 'seloger', 'logicimmo', 'pap']),
        titre=bien.titre,
        description=bien.description,
        prix=bien.prix,
        date_publication=timezone.now(),
        campagne=campagne
    )

    SiteVitrine.objects.create(
        bien=bien,
        publie=True,
        date_publication=timezone.now(),
        slug=f"bien-{bien.id}-dakar",
        meta_description=f"Annonce immobilière: {bien.titre}"
    )

print(f"✅ {len(list(Annonce.objects.all()))} annonces créées")

# Email marketing
email = EmailMarketing.objects.create(
    campagne=campagne,
    objet="Découvrez nos meilleures propriétés à Dakar",
    corps_html="<h2>Bienvenue chez Immovia</h2><p>Découvrez nos propriétés sélectionnées au Sénégal</p>",
    corps_texte="Bienvenue chez Immovia. Découvrez nos propriétés sélectionnées.",
    date_envoi=timezone.now()
)

for client in clients[:8]:
    DestinataireEmail.objects.create(
        email=email,
        client=client,
        envoye=True,
        ouvert=random.choice([True, False])
    )

PublicationSociale.objects.create(
    campagne=campagne,
    reseau=random.choice(['facebook', 'instagram', 'whatsapp']),
    message="Retrouvez nos meilleures propriétés sur Immovia! 🏠 #Immobilier #Dakar #Senegal",
    date_publication=timezone.now()
)

print(f"✅ Campagne marketing complète")

# Rendez-vous sénégalais
for i in range(6):
    creneau = CreneauDisponible.objects.create(
        agent=user,
        bien=random.choice(biens),
        date_debut=timezone.now() + timedelta(days=i, hours=10),
        date_fin=timezone.now() + timedelta(days=i, hours=11),
        notes="Visite guidée - merci de confirmer"
    )

    rdv = RendezVous.objects.create(
        creneau=creneau,
        client=random.choice(clients),
        statut=random.choice(['planifie', 'confirme', 'effectue'])
    )

    if rdv.statut == 'effectue':
        RapportVisite.objects.create(
            rendez_vous=rdv,
            present=True,
            impressions=random.choice([
                "Client très intéressé",
                "Bien correspond aux critères",
                "Demande délai de réflexion",
                "Visite sans suite"
            ]),
            interet=random.randint(1, 5),
            agent=user
        )

print(f"✅ {len(list(RendezVous.objects.all()))} rendez-vous créés")

# Transactions sénégalaises
for i in range(3):
    dossier = DossierTransaction.objects.create(
        bien=random.choice(biens),
        acheteur=random.choice(clients),
        vendeur=random.choice(clients),
        agent=user,
        etape=random.choice(['initial', 'avant_contrat', 'notaire', 'acompte', 'acte_final', 'cloture'])
    )

    Offre.objects.create(
        dossier=dossier,
        montant=dossier.bien.prix * random.uniform(0.85, 1.0),
        conditions="Financement à confirmer",
        statut=random.choice(['proposee', 'acceptee', 'refusee']),
        auteur=user
    )

    DocumentTransaction.objects.create(
        dossier=dossier,
        type_document=random.choice(['contrat', 'diagnostic', 'acte', 'identite']),
        fichier=None,
        est_signe=random.choice([True, False])
    )

    HistoriqueNotaire.objects.create(
        dossier=dossier,
        notes="Dossier en cours de traitement",
        etape="Phase notariale",
        notaire="Maître Notaire Dakar",
        complet=False
    )

print(f"✅ {len(list(DossierTransaction.objects.all()))} dossiers de transaction créés")

print("\n" + "="*60)
print("✅ DONNÉES DE TEST SÉNÉGALAISES CRÉÉES AVEC SUCCÈS!")
print("="*60)
print(f"✓ {len(biens)} biens immobiliers")
print(f"✓ {len(clients)} clients")
print(f"✓ {len(list(Bail.objects.all()))} baux de location")
print(f"✓ {len(list(Facture.objects.all()))} factures")
print(f"✓ {len(list(RendezVous.objects.all()))} rendez-vous")
print(f"✓ {len(list(DossierTransaction.objects.all()))} transactions")
print("="*60)
