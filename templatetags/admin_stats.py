from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def sum_object_counts(models):
    """Somme les object_count de tous les modèles d'une app"""
    return sum(model['model'].objects.count() for model in models)

@register.filter
def admin_urlname(opts, action):
    """Génère le nom d'URL admin pour un modèle et une action"""
    return f'admin:{opts.app_label}_{opts.model_name}_{action}'

@register.filter
def remove(value, arg):
    """Supprime toutes les occurrences de arg dans value"""
    return str(value).replace(str(arg), '')