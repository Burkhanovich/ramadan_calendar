from django.urls import path
from .views import (
    regions_list_view,
    district_list_view,
    ramadan_time,
    region_detail,
    categories_list,
    prayer_times_api,
    category_detail,
    surah_list,
    surah_detail,
)

urlpatterns = [
    path('regions/', regions_list_view, name='regions'),
    path('region_detail/<int:pk>', region_detail, name='region_detail'),
    path('districts/<int:pk>/', district_list_view, name='districts'),
    path('ramadan_time/<int:d_id>', ramadan_time, name='ramadan_time'),
    path('categories_list/', categories_list, name='categories_list'),
    path('category_detail/<int:pk>/', category_detail, name='category_detail'),
    path('surah_list/', surah_list, name='surah_list'),
    path('surah_detail/<int:pk>', surah_detail, name='surah_detail'),
    path('prayer_times_api/<int:region_id>', prayer_times_api, name='prayer_times_api')
]