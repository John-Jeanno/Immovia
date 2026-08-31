from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.db.models import Sum, Count, Q, Avg, DecimalField, F, Max, Min
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal

from biens.models import BienImmobilier
from clients.models import Client
from transactions.models import DossierTransaction, Offre
from rendezvous.models import RendezVous, RapportVisite
from chantiers.models import Chantier
from comptabilite.models import Facture, Operation


class PresentationView(TemplateView):
    template_name = 'presentation.html'

def admin_required(user):
    return user.is_authenticated and user.is_staff

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(admin_required), name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        
        # ==================== STATISTIQUES BIENS ====================
        context['total_biens'] = BienImmobilier.objects.count()
        context['biens_disponibles'] = BienImmobilier.objects.filter(statut='disponible').count()
        context['biens_reserves'] = BienImmobilier.objects.filter(statut='reserve').count()
        context['biens_vendus'] = BienImmobilier.objects.filter(statut='vendu_loue').count()
        context['biens_negociation'] = BienImmobilier.objects.filter(statut='negociation').count()
        
        # Statistiques de prix
        biens_stats = BienImmobilier.objects.aggregate(
            prix_moyen=Avg('prix'),
            prix_total=Sum('prix'),
            surface_moyenne=Avg('surface')
        )
        context['prix_moyen_biens'] = biens_stats.get('prix_moyen', 0)
        context['prix_total_biens'] = biens_stats.get('prix_total', 0)
        context['surface_moyenne'] = biens_stats.get('surface_moyenne', 0)
        
        # Distribution par type
        context['biens_par_type'] = BienImmobilier.objects.values('type_bien').annotate(count=Count('id'))
        context['biens_par_ville'] = BienImmobilier.objects.values('ville').annotate(count=Count('id')).order_by('-count')[:10]
        
        # ==================== STATISTIQUES CLIENTS ====================
        context['total_clients'] = Client.objects.count()
        context['clients_acheteurs'] = Client.objects.filter(type_client='ACH').count()
        context['clients_vendeurs'] = Client.objects.filter(type_client='VEN').count()
        context['clients_locataires'] = Client.objects.filter(type_client='LOC').count()
        context['clients_proprietaires'] = Client.objects.filter(type_client='PRO').count()
        
        # Budget moyen par client
        clients_budget = Client.objects.aggregate(
            budget_moyen=Avg('budget'),
            budget_total=Sum('budget')
        )
        context['budget_moyen_client'] = clients_budget.get('budget_moyen', 0)
        context['budget_total_clients'] = clients_budget.get('budget_total', 0)
        
        # ==================== STATISTIQUES TRANSACTIONS ====================
        context['total_transactions'] = DossierTransaction.objects.count()
        context['transactions_en_cours'] = DossierTransaction.objects.exclude(
            etape__in=['cloture']
        ).count()
        context['transactions_clotureées'] = DossierTransaction.objects.filter(etape='cloture').count()
        
        # Distribution par étape
        context['transactions_par_etape'] = DossierTransaction.objects.values('etape').annotate(count=Count('id'))
        
        # Montant moyen des offres
        offres_stats = Offre.objects.aggregate(
            montant_moyen=Avg('montant'),
            montant_total=Sum('montant'),
            offres_acceptees=Count('id', filter=Q(statut='acceptee'))
        )
        context['montant_moyen_offre'] = offres_stats.get('montant_moyen', 0)
        context['montant_total_offres'] = offres_stats.get('montant_total', 0)
        context['offres_acceptees'] = offres_stats.get('offres_acceptees', 0)
        
        # ==================== STATISTIQUES RENDEZ-VOUS ====================
        context['total_rendez_vous'] = RendezVous.objects.count()
        context['rendez_vous_a_venir'] = RendezVous.objects.filter(
            creneau__date_debut__gte=now
        ).count()
        context['rendez_vous_effectues'] = RendezVous.objects.filter(statut='effectue').count()
        context['rendez_vous_annules'] = RendezVous.objects.filter(statut='annule').count()
        
        # Taux de conversion
        rapports_visite = RapportVisite.objects.filter(present=True).count()
        context['taux_presence_rdv'] = round(
            (rapports_visite / context['rendez_vous_effectues'] * 100) if context['rendez_vous_effectues'] > 0 else 0, 2
        )
        
        # ==================== STATISTIQUES CHANTIERS ====================
        context['total_chantiers'] = Chantier.objects.count()
        context['chantiers_termines'] = Chantier.objects.filter(etat_chantier__in=['termine', 'livre']).count()
        context['chantiers_en_cours'] = Chantier.objects.filter(etat_chantier__in=['en_cours', 'finition']).count()
        context['chantiers_planifies'] = Chantier.objects.filter(etat_chantier__in=['planifie', 'preparation']).count()
        context['chantiers_en_retard'] = Chantier.objects.filter(etat_chantier='en_retard').count()
        
        # Budget chantiers
        chantiers_stats = Chantier.objects.aggregate(
            budget_total=Sum('budget'),
            budget_depense=Sum('budget_depense'),
            progression_moyenne=Avg('pourcentage_avancement')
        )
        context['budget_total_chantiers'] = chantiers_stats.get('budget_total', 0)
        context['budget_depense_chantiers'] = chantiers_stats.get('budget_depense', 0)
        context['budget_restant_chantiers'] = (context['budget_total_chantiers'] or 0) - (context['budget_depense_chantiers'] or 0)
        context['progression_moyenne_chantiers'] = round(chantiers_stats.get('progression_moyenne') or 0, 2)
        
        # Calcul du taux d'utilisation
        try:
            budget_total = float(context['budget_total_chantiers'] or 0)
            budget_depense = float(context['budget_depense_chantiers'] or 0)
            if budget_total > 0:
                context['taux_utilisation_chantiers'] = round((budget_depense / budget_total) * 100, 1)
            else:
                context['taux_utilisation_chantiers'] = 0
        except (TypeError, ValueError, ZeroDivisionError):
            context['taux_utilisation_chantiers'] = 0
        
        # ==================== STATISTIQUES COMPTABILITÉ ====================
        factures_stats = Facture.objects.aggregate(
            montant_total=Sum('montant_ttc'),
            nombre=Count('id'),
            montant_moyen=Avg('montant_ttc')
        )
        context['montant_total_factures'] = factures_stats.get('montant_total', 0)
        context['nombre_factures'] = factures_stats.get('nombre', 0)
        context['montant_moyen_factures'] = factures_stats.get('montant_moyen', 0)
        
        # Operations comptables (via le modèle Operation, pas Transaction)
        operations_entrees = Operation.objects.filter(
            categorie__type_categorie='recette'
        ).aggregate(total=Sum('montant'))
        
        operations_sorties = Operation.objects.filter(
            categorie__type_categorie='depense'
        ).aggregate(total=Sum('montant'))
        
        context['total_entrees'] = operations_entrees.get('total', 0) or 0
        context['total_sorties'] = operations_sorties.get('total', 0) or 0
        
        # Calcul du solde net avec sécurité
        try:
            total_entrees = float(context['total_entrees'] or 0)
            total_sorties = float(context['total_sorties'] or 0)
            context['solde_net'] = round(total_entrees - total_sorties, 2)
        except (TypeError, ValueError):
            context['solde_net'] = 0
        
        # ==================== DONNÉES RÉCENTES ====================
        context['biens_recents'] = BienImmobilier.objects.order_by('-date_creation')[:5]
        
        context['rendez_vous_prochains'] = RendezVous.objects.filter(
            creneau__date_debut__gte=now
        ).order_by('creneau__date_debut')[:5]
        
        context['transactions_recentes'] = DossierTransaction.objects.order_by('-date_creation')[:5]
        
        context['chantiers_recents'] = Chantier.objects.order_by('-date_creation')[:5]
        
        # ==================== MÉTRIQUES DE PERFORMANCE ====================
        # Taux de conversion client
        clients_avec_transactions = Client.objects.filter(
            Q(achats__isnull=False) | Q(ventes__isnull=False)
        ).distinct().count()
        context['taux_conversion_client'] = round(
            (clients_avec_transactions / context['total_clients'] * 100) if context['total_clients'] > 0 else 0, 2
        )
        
        # Vitesse moyenne de vente (jours)
        transactions_terminees = DossierTransaction.objects.filter(
            etape='cloture'
        ).annotate(
            jours_transaction=Coalesce(
                (timezone.now() - timezone.make_aware(timezone.datetime.combine(timezone.now().date(), timezone.datetime.min.time()))),
                timedelta(0),
                output_field=DecimalField()
            )
        )
        context['nombre_transactions_terminees'] = transactions_terminees.count()
        
        # ==================== INDICATEURS GLOBAUX AVANCÉS ====================
        # 1. KPI Synthétique - Performance Commerciale
        prix_moyen_transaction = Offre.objects.filter(
            statut='acceptee'
        ).aggregate(avg=Avg('montant'))['avg'] or 0
        
        context['prix_moyen_transaction'] = prix_moyen_transaction
        context['taux_acceptation_offres'] = round(
            (offres_stats.get('offres_acceptees', 0) / Offre.objects.count() * 100) if Offre.objects.count() > 0 else 0, 2
        )
        
        # 2. Santé Financière Globale
        # Revenus vs Dépenses
        factures_payees = Facture.objects.filter(statut='payee').aggregate(
            total=Sum('montant_ttc')
        )['total'] or 0
        
        context['revenus_realises'] = factures_payees
        context['ratio_sante_financiere'] = round(
            (context['total_entrees'] / context['total_sorties'] * 100) if context['total_sorties'] > 0 else 0, 2
        )
        
        # 3. Performance des Chantiers
        chantiers_en_retard_percent = round(
            (context['chantiers_en_retard'] / context['total_chantiers'] * 100) if context['total_chantiers'] > 0 else 0, 2
        )
        context['chantiers_en_retard_percent'] = chantiers_en_retard_percent
        context['chantiers_a_risque'] = Chantier.objects.filter(
            etat_chantier__in=['en_retard', 'preparation'],
            budget_depense__gt=F('budget') * 0.8
        ).count()
        
        # 4. Indicateurs de Performance - Rendez-vous
        if context['rendez_vous_effectues'] > 0:
            context['taux_conversion_rdv'] = round(
                (transactions_terminees.count() / context['rendez_vous_effectues'] * 100), 2
            )
        else:
            context['taux_conversion_rdv'] = 0
            
        # 5. Portfolio Value - Valeur globale du portefeuille
        valeur_portfolio = (context['prix_total_biens'] or 0) + (context['budget_total_chantiers'] or 0)
        context['valeur_portfolio'] = valeur_portfolio
        
        # 6. Activité mensuelle (30 derniers jours)
        trente_jours_avant = now - timedelta(days=30)
        context['biens_ajoutes_mois'] = BienImmobilier.objects.filter(
            date_creation__gte=trente_jours_avant
        ).count()
        context['transactions_creees_mois'] = DossierTransaction.objects.filter(
            date_creation__gte=trente_jours_avant
        ).count()
        context['clients_ajoutes_mois'] = Client.objects.filter(
            date_creation__gte=trente_jours_avant
        ).count()
        context['factures_creees_mois'] = Facture.objects.filter(
            date_emission__gte=trente_jours_avant
        ).count()
        
        # 7. Métriques de productivité
        context['ratio_clients_actifs'] = round(
            (clients_avec_transactions / context['total_clients'] * 100) if context['total_clients'] > 0 else 0, 2
        )
        context['biens_par_client'] = round(
            (context['total_biens'] / context['total_clients']) if context['total_clients'] > 0 else 0, 2
        )
        context['transactions_par_bien'] = round(
            (context['total_transactions'] / context['total_biens']) if context['total_biens'] > 0 else 0, 2
        )
        
        # 8. Analyse de la demande
        context['budget_demande_total'] = context['budget_total_clients']
        context['ratio_offre_demande'] = round(
            (context['prix_total_biens'] / context['budget_demande_total'] * 100) if context['budget_demande_total'] and context['budget_demande_total'] > 0 else 0, 2
        )
        
        # 9. Statuts critiques à surveiller
        context['biens_negociation_percent'] = round(
            (context['biens_negociation'] / context['total_biens'] * 100) if context['total_biens'] > 0 else 0, 2
        )
        context['transactions_en_retard'] = DossierTransaction.objects.filter(
            date_maj__lt=now - timedelta(days=30),
            etape__in=['initial', 'avant_contrat', 'notaire']
        ).count()
        
        # 10. Distribution d'âge du portefeuille
        biens_moins_3mois = BienImmobilier.objects.filter(
            date_creation__gte=now - timedelta(days=90)
        ).count()
        biens_3_6mois = BienImmobilier.objects.filter(
            date_creation__gte=now - timedelta(days=180),
            date_creation__lt=now - timedelta(days=90)
        ).count()
        biens_plus_6mois = BienImmobilier.objects.filter(
            date_creation__lt=now - timedelta(days=180)
        ).count()
        
        context['biens_distribution_age'] = {
            'moins_3_mois': biens_moins_3mois,
            'age_3_6_mois': biens_3_6mois,
            'plus_6_mois': max(context['total_biens'] - biens_moins_3mois - biens_3_6mois, 0)
        }
        
        # 11. Prévisions rapides
        if context['biens_ajoutes_mois'] > 0:
            context['projection_biens_annee'] = context['biens_ajoutes_mois'] * 12
        else:
            context['projection_biens_annee'] = 0
            
        if context['transactions_creees_mois'] > 0:
            context['projection_transactions_annee'] = context['transactions_creees_mois'] * 12
        else:
            context['projection_transactions_annee'] = 0
        
        # 12. Score de santé global (0-100)
        score_elements = []
        # Santé financière (0-30 points)
        if context['ratio_sante_financiere'] >= 100:
            score_elements.append(30)
        elif context['ratio_sante_financiere'] >= 50:
            score_elements.append(20)
        elif context['ratio_sante_financiere'] > 0:
            score_elements.append(10)
        else:
            score_elements.append(0)
            
        # Conversion clients (0-25 points)
        score_elements.append(min(context['ratio_clients_actifs'] / 4, 25))
        
        # Chantiers à temps (0-25 points)
        if chantiers_en_retard_percent < 10:
            score_elements.append(25)
        elif chantiers_en_retard_percent < 30:
            score_elements.append(15)
        else:
            score_elements.append(5)
            
        # Transactions complétées (0-20 points)
        score_elements.append(min((context['transactions_clotureées'] / max(context['total_transactions'], 1)) * 20, 20))
        
        context['score_sante_global'] = round(sum(score_elements), 1)
        context['couleur_score'] = 'danger' if context['score_sante_global'] < 40 else 'warning' if context['score_sante_global'] < 70 else 'success'
        
        # 13. Données pour graphiques (top 10)
        context['top_villes'] = BienImmobilier.objects.values('ville').annotate(
            count=Count('id'),
            prix_moyen=Avg('prix')
        ).order_by('-count')[:10]
        
        context['top_clients_actifs'] = Client.objects.annotate(
            nb_transactions=Count('achats') + Count('ventes')
        ).filter(nb_transactions__gt=0).order_by('-nb_transactions')[:10]
        
        # 14. Alertes et notifications
        context['alertes'] = []
        if context['chantiers_en_retard'] > 0:
            context['alertes'].append({
                'type': 'warning',
                'message': f"{context['chantiers_en_retard']} chantier(s) en retard"
            })
        if context['transactions_en_retard'] > 0:
            context['alertes'].append({
                'type': 'warning',
                'message': f"{context['transactions_en_retard']} transaction(s) stagnante(s)"
            })
        if context['chantiers_a_risque'] > 0:
            context['alertes'].append({
                'type': 'danger',
                'message': f"{context['chantiers_a_risque']} chantier(s) à risque budgétaire"
            })
        if context['ratio_sante_financiere'] < 100:
            context['alertes'].append({
                'type': 'danger',
                'message': f"Sorties > Entrées: {context['ratio_sante_financiere']}%"
            })
        
        return context