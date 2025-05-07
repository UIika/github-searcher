from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import search_github, clear_cache


urlpatterns = [
    path('search', search_github, name='search-github'),
    path('clear-cache', clear_cache, name='clear-cache'),
]