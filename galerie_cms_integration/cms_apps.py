from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import url
from .views import LampeListView, LampeDetailView, accueil
from .menu import GalerieMenu

@apphook_pool.register  # register the application
class GalerieAppHook(CMSApp):
	app_name = "galerieapp"
	name = _("Application galerie")

	def get_urls(self, page=None, language=None, **kwargs):
		return [
			url(r'^$', accueil.as_view(), name='accueil'),
			url(r'^lampes/$', LampeListView.as_view(), name='LampeListView'),
			url(r'^lampes/(?P<slug>[\w-]+)/?$', LampeDetailView.as_view(), name='LampeDetailView'),
			]
	#def get_menus(self, page=None, language=None, **kwargs):
	#	return [GalerieMenu]

