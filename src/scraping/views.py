from django.shortcuts import render

from .models import Vacancy
from .forms import FindForm


def home_view(request):
    city = request.GET.get('city')
    language = request.GET.get('language')
    query = []
    form = FindForm()
    if city or language:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if language:
            _filter['language__name'] = language
            query = Vacancy.objects.filter(**_filter)
    context = {
        'query': query,
        'form': form
    }
    return render(request, 'scraping/home.html', context)
