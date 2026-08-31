from django import template

register = template.Library()

@register.filter
def get_value(dict_obj, key):
    """Accède à une valeur dans un dictionnaire ou QueryDict"""
    if hasattr(dict_obj, 'get'):
        return dict_obj.get(key, '')
    return getattr(dict_obj, key, '')


@register.filter
def model_count(model_context):
    """Retourne le nombre réel d'objets du modèle fourni par l'admin Django."""
    try:
        model = model_context.get('model') if hasattr(model_context, 'get') else model_context
        return model._default_manager.count()
    except (AttributeError, TypeError, ValueError):
        return 0