from galerie_cms_integration.models import Loc, Groupe
from django.contrib.gis.geos import GEOSGeometry, Point


l = Loc()

l.geolocalisation = Point(12.4604, 43.9420)

l.save()
Loc.objects.all()


c=Loc.objects.filter(geolocalisation='Point(12.4604 43.9420)')
c.delete()

d=Loc.objects.all()
d.delete()

l.geolocalisation=GEOSGeometry('POINT(%s %s)' % (1,1))


import django
django.get_version()
from django.contrib.gis import geos
geos.geos_version()