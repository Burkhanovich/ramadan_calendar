from django.contrib import admin
from .models import Region, DistrictTime, DefaultTime, Category, Surah

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


@admin.register(DistrictTime)
class DistrictTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'region__name', 'name', 'time_difference')
    search_fields = ('region__name', 'name')

@admin.register(DefaultTime)
class DefaultTimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'date',)
    sortable_by = 'date'
    search_fields = ('date', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Surah)
class Surah(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'categories')
    filter_horizontal = ('categories', )







