from django.contrib import admin
from django.utils.html import format_html

from .models import BienImmobilier, ImageBien, Mandat


class ImageBienInline(admin.TabularInline):
    model = ImageBien
    extra = 1


@admin.register(BienImmobilier)
class BienImmobilierAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ville', 'statut', 'prix', 'latitude', 'longitude')
    list_filter = ('statut', 'ville', 'type_bien')
    search_fields = ('titre', 'adresse', 'ville')
    inlines = [ImageBienInline]
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'type_bien', 'statut', 'description')
        }),
        ('Localisation', {
            'fields': ('adresse', 'code_postal', 'ville', 'latitude', 'longitude')
        }),
        ('Caractéristiques', {
            'fields': ('surface', 'nombre_pieces', 'prix')
        }),
    )
    readonly_fields = ('date_creation', 'date_mise_a_jour')

    class Media:
        css = {
            'all': [
                'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
            ]
        }
        js = [
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
        ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['adresse'].help_text = 'Adresse exacte + ville. La carte se mettra à jour automatiquement.'
        return form


@admin.register(Mandat)
class MandatAdmin(admin.ModelAdmin):
    list_display = ('bien', 'type_mandat', 'actif')
    search_fields = ('bien__titre',)


@admin.register(ImageBien)
class ImageBienAdmin(admin.ModelAdmin):
    list_display = ('bien', 'legende', 'image')
    search_fields = ('bien__titre', 'legende')
