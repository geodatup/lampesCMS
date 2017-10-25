from django import template

from galerie_cms_integration.models import Lampe
from django.template.loader import get_template

register = template.Library()



@register.inclusion_tag('lampeList.html', takes_context=True)
def show_lampe_index(context, slug):
    request = context['request']
    latest_lampe_list = Lampe.objects.exclude(slug=slug)
    
    return {'latest_lampe_list': latest_lampe_list, 'request':request}

