from django.urls import path

from .views import search_github, clear_cache


urlpatterns = [
    path('search', search_github, name='search-github'),
    path('clear-cache', clear_cache, name='clear-cache'),
]