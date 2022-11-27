from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_view(request):
    form = FindForm()
    context = {
        'form': form
    }
    return render(request, 'scraping/home.html', context)


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    query = []
    context = {'city': city, 'language': language, 'form': form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language
            query = Vacancy.objects.filter(**_filter)
        paginator = Paginator(query, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)


def about_view(request):
    return render(request, 'scraping/about.html')
