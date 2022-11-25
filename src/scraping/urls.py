from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('list', views.list_view, name='list'),
]