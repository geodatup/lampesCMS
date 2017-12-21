from galerie_cms_integration.models import Localisation
from django.contrib.gis.geos import GEOSGeometry, Point
l = Localisation()

l.geolocalisation = Point(12.4604, 43.9420)

l.save()
Localisation.objects.all()


from galerie_cms_integration.models import Localisation
from django.contrib.gis.geos import GEOSGeometry, Point

Localisation.objects.all()

d=Localisation.objects.all()
d.delete()


