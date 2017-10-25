from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
from cms.toolbar.items import Break, SubMenu
from cms.utils.urlutils import admin_reverse
from cms.cms_toolbars import ADMIN_MENU_IDENTIFIER, ADMINISTRATION_BREAK
from .models import Lampe

@toolbar_pool.register
class GalerieToolbar(CMSToolbar):
    supported_apps = (
        #'galerie',
        'galerie_cms_integration',
    )

    watch_models = [Lampe]

    def populate(self):

        admin_menu = self.toolbar.get_or_create_menu(ADMIN_MENU_IDENTIFIER, _('Admin'))

        position = admin_menu.get_alphabetical_insert_position(
            _('Lampe'),
            SubMenu
        )

        if not position:
            position = admin_menu.find_first(Break, identifier=ADMINISTRATION_BREAK) + 1
            admin_menu.add_break('custom-break', position=position)
        #if not self.is_current_app:
        #    return
        #menu = self.toolbar.get_or_create_menu('Galerie-app', _('Galerie'))
        menu = admin_menu.get_or_create_menu('Galerie-app', _('Lampe ...'), position=position)
#
        menu.add_sideframe_item(
            name=_('Toutes les lampes'),
            url=admin_reverse('galerie_cms_integration_lampe_changelist'),
        )
        menu.add_modal_item(
            name=_('Ajouter une lampe'),
            url=admin_reverse('galerie_cms_integration_lampe_add'),
        )

