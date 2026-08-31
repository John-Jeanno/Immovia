"""
Utilitaires pour les actions personnalisées de l'administrateur Django
"""
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin.options import TO_FIELD_VAR


def make_delete_action(model_name_singular, model_name_plural=None):
    """
    Crée une action personnalisée de suppression avec confirmation
    
    Args:
        model_name_singular: Nom singulier du modèle (ex: 'Client')
        model_name_plural: Nom pluriel du modèle (ex: 'Clients') - auto-généré si None
    """
    if model_name_plural is None:
        model_name_plural = model_name_singular + 's'
    
    def delete_selected_with_confirmation(modeladmin, request, queryset):
        # Si c'est une confirmation POST
        if request.POST.get('confirm_delete'):
            count = queryset.count()
            queryset.delete()
            message = f"{count} {model_name_singular.lower()}(s) supprimé(s) avec succès."
            modeladmin.message_user(request, message, messages.SUCCESS)
            return
        
        # Sinon, afficher la page de confirmation
        context = {
            'title': 'Confirmer la suppression',
            'queryset': queryset,
            'model_name': model_name_singular,
            'opts': modeladmin.model._meta,
        }
        return render(request, 'admin/confirm_delete.html', context)
    
    delete_selected_with_confirmation.short_description = f"Supprimer les {model_name_plural.lower()} sélectionnés"
    return delete_selected_with_confirmation


def get_admin_actions_buttons(obj, modeladmin):
    """
    Génère les boutons d'action (Modifier, Supprimer) pour une ligne d'admin
    
    Args:
        obj: L'objet à éditer/supprimer
        modeladmin: L'instance ModelAdmin
    
    Returns:
        HTML formaté avec les boutons d'action
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.model_name
    
    # URL de modification
    change_url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
    
    # URL de suppression
    delete_url = reverse(f'admin:{app_label}_{model_name}_delete', args=[obj.pk])
    
    return format_html(
        '<div style="white-space: nowrap;">'
        '<a class="button" style="background-color: #417690; padding: 5px 10px; margin-right: 5px; '
        'text-decoration: none; color: white; border-radius: 4px; display: inline-block; font-size: 11px;" '
        'href="{}">'
        '<i class="fas fa-edit"></i> Modifier'
        '</a>'
        '<a class="button" style="background-color: #ba2121; padding: 5px 10px; '
        'text-decoration: none; color: white; border-radius: 4px; display: inline-block; font-size: 11px;" '
        'href="{}" onclick="return confirm(\'Êtes-vous sûr de vouloir supprimer cet élément ?\');">'
        '<i class="fas fa-trash"></i> Supprimer'
        '</a>'
        '</div>',
        change_url,
        delete_url
    )

