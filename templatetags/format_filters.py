from django import template

register = template.Library()


@register.filter
def format_currency(value):
    """
    Formatte un nombre avec des points comme séparateurs de milliers.
    Ex: 1000000 -> 1.000.000
    """
    if value is None:
        return ""
    
    try:
        # Convertir en nombre entier
        num = int(float(value))
        
        # Formater avec des points comme séparateurs
        return "{:,}".format(num).replace(",", ".")
    except (ValueError, TypeError):
        return value


@register.filter
def format_amount(value):
    """
    Alias pour format_currency. Formatte un montant avec des points comme séparateurs.
    Ex: 24000000 -> 24.000.000
    """
    return format_currency(value)


@register.filter
def sum(value, arg=None):
    """
    Calcule la somme d'un attribut spécifique sur une liste d'objets.
    Utilisation: {{ items|sum:'field_name' }}
    """
    if not value:
        return 0
    
    if arg is None:
        # Si pas d'argument, faire la somme simple
        try:
            return sum(float(item) if isinstance(item, (int, float, str)) else 0 for item in value)
        except (ValueError, TypeError):
            return 0
    
    # Si un argument est fourni, accumuler la valeur de cet attribut
    try:
        total = 0
        for item in value:
            if hasattr(item, arg):
                attr_value = getattr(item, arg)
                total += float(attr_value) if attr_value else 0
        return total
    except (ValueError, TypeError, AttributeError):
        return 0
