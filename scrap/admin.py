from django.contrib import admin
from .models import Ads, Categories


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ['header', 'price', 'city', 'position']
    list_filter = ['category__name']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'url']
