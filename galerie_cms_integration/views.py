from django.shortcuts import render
from django.views import generic
from .models import Lampe
# Create your views here.


class accueil(generic.ListView):
    model = Lampe
    template_name = 'accueil.html'
    context_object_name = 'latest_lampe_list'
    #queryset = Oeuvre.objects.all().order_by('rubrique__annee') #tri par annee de rubrique
    queryset = Lampe.objects.all().order_by('?') #tri aléatoire


class LampeListView(generic.ListView):
    template_name = 'lampeIndex.html'
    context_object_name = 'latest_lampe_list'
    queryset = Lampe.objects.all()
    

class LampeDetailView(generic.DetailView):
    model = Lampe
    context_object_name = 'lampe'
    template_name = 'lampeDetail.html'