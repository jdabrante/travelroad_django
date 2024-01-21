from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from .models import Place


def index(request):
    wished = Place.objects.filter(visited=False)
    visited = Place.objects.filter(visited=True)
    template = loader.get_template('places/index.html')
    context = {
        'wished': wished,
        'visited': visited,
    }
    return HttpResponse(template.render(context, request))

def visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'places/visited.html', dict(visited=visited))

def wished(request):
    wished = Place.objects.filter(visited=False)
    return render(request, 'places/wished.html', dict(wished=wished))
