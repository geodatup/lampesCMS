from django.db import models
from filer.fields.image import FilerImageField
from djangocms_text_ckeditor.fields import HTMLField
from django.core.urlresolvers import reverse
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from django.contrib.gis.db import models
from urllib.error import URLError
from django.contrib.gis.geos import GEOSGeometry, Point



class Localisation(models.Model):
	nom = models.CharField(max_length=30)
	adresse = models.CharField(blank=True, null=True, max_length=100)
	ville = models.CharField(blank=True, null=True, max_length=100)
	geocodeAdresse =  models.CharField(blank=True, null=True, max_length=200)
	geolocalisation = models.PointField(srid=4326, blank=True, null=True)

	def __str__(self):
		return self.nom

	def save(self, *args, **kwargs):
		if not self.geolocalisation:
			address = u'%s %s' % (self.ville, self.adresse)
			geolocator = Nominatim(country_bias='France',timeout=10)
			try:
				result = geolocator.geocode(address,  exactly_one = True)
			except (URLError, ValueError):				
				pass
			else:
				#print (address, result)
				self.geolocalisation = GEOSGeometry('POINT(%s %s)' % (result.longitude, result.latitude)).ewkt				
				resultAddress = result.address
				self.geocodeAdresse = resultAddress
		super(Localisation, self).save()

class Loc(models.Model):
	geolocalisation = models.PointField(srid=4326, blank=True, null=True)


class Groupe(models.Model):
	nom = models.CharField(max_length=30)
	description = HTMLField(blank=True, null=True)
	def __str__(self):
		return self.nom

# Create your models here.
class Lampe(models.Model):
	nom = models.CharField(max_length=30)
	hauteur = models.PositiveIntegerField(blank=True, null=True)
	largeur_socle =  models.PositiveIntegerField(blank=True, null=True)
	diametre = models.PositiveIntegerField(blank=True, null=True)
	materiaux = models.CharField(blank=True, null=True, max_length=100)
	ampoule = models.CharField(blank=True, null=True, max_length=100)
	cable = models.CharField(blank=True, null=True, max_length=100)
	electrification = models.CharField(blank=True, null=True, max_length=100)
	description = HTMLField(blank=True, null=True)
	groupe = models.ManyToManyField(Groupe, related_name='lampes')
	localisation = models.ForeignKey(Localisation, related_name='localisation',blank=True, null=True)
	slug = models.SlugField(
		u'slug',
		blank=False,
		default='',
		help_text=u'mettre un slug unique pour cette lampe',
		max_length=64,
	)


	def __str__(self):
		return self.nom

	def get_absolute_url(self):
		return reverse('galerieapp:LampeDetailView', kwargs={'slug': self.slug, })

        

class LampeImage(models.Model):
	lampe = models.ForeignKey(Lampe, related_name='photos')
	photo = FilerImageField(blank=True, null=True,on_delete=models.SET_NULL,)
