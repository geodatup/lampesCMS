from django.contrib import admin
from django.contrib.gis import admin

# Register your models here.
from .models import Lampe, LampeImage, Groupe, Localisation, Loc



class LampeImageInline(admin.TabularInline):
    model = LampeImage
    extra = 3

class LampeAdmin(admin.ModelAdmin):
    inlines = [ LampeImageInline, ]
    fieldsets = [
    	(None, {'fields': (
          'nom',('hauteur','largeur_socle','diametre'),          
          'description',
          ('materiaux','cable','electrification', 'ampoule'),
          'groupe',
          'localisation' 
        )         
        }),
        ('Options Avancées', {
            'classes': ('collapse',),
            'fields': ('slug',),
        }),
    ]
    prepopulated_fields = {'slug': ('nom','hauteur','largeur_socle') }

admin.site.register(Lampe, LampeAdmin)
admin.site.register(Groupe)
admin.site.register(Localisation, admin.GeoModelAdmin)
admin.site.register(Loc, admin.GeoModelAdmin)


