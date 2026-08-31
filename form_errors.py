def iter_form_error_messages(errors):
    """Retourne les erreurs de formulaire sous forme de texte lisible."""
    for field, field_errors in errors.items():
        label = field.replace('_', ' ').capitalize() if field != '__all__' else 'Formulaire'
        for error in field_errors:
            yield f"{label}: {error}"


def iter_formset_error_messages(formset_errors, prefix='Erreur image'):
    """Retourne les erreurs d'un formset sans exposer son HTML interne."""
    for index, errors in enumerate(formset_errors, start=1):
        for field, field_errors in errors.items():
            for error in field_errors:
                if field == '__all__':
                    yield f"{prefix} {index}: {error}"
                else:
                    label = field.replace('_', ' ').capitalize()
                    yield f"{prefix} {index} ({label}): {error}"