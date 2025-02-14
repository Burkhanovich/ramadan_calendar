from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from .models import Region, DistrictTime, DefaultTime, Category, Surah
from .serializers import (
    DistrictTimeSerializer,
    RegionSerializer,
    DefaultTimeSerializer,
    CategorySerializer,
    SurahSerializer,
)
import requests


@api_view(['GET', ])
def regions_list_view(request):
    qs=Region.objects.all()
    serializer=RegionSerializer(qs, many=True)
    return Response(serializer.data)

@api_view
def region_detail(request, id):
    obj=get_object_or_404(Region, id=id)
    serializer=RegionSerializer(obj)
    return Response(serializer.data)

@api_view(['GET'])
def district_list_view(request, pk):
    qs=DistrictTime.objects.filter(region__id=pk)
    serializer=DistrictTimeSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ramadan_time(request, d_id):
    obj = get_object_or_404(DistrictTime, id=d_id)
    default_times = DefaultTime.objects.all()
    time_difference = timedelta(minutes=obj.time_difference)
    data={}
    if not default_times.exists():
        return Response({"error": "DefaultTime ma'lumotlari topilmadi!"}, status=status.HTTP_404_NOT_FOUND)
    for date_time in default_times:
        saharlik=(datetime.combine(date_time.date, date_time.saharlik)+time_difference).time()
        iftorlik=(datetime.combine(date_time.date, date_time.iftorlik)+time_difference).time()
        data[f'{date_time.date}']={'saharlik':saharlik, 'iftorlik': iftorlik}
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'], )
def categories_list(request):
    categories=Category.objects.all()
    serializer=CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET',])
def category_detail(request, id):
    obj=get_object_or_404(Category, id=id)
    serializer=CategorySerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', ])
def surah_list(request):
    qs=Surah.objects.all()
    serializer=SurahSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', ])
def surah_detail(request, id):
    obj=get_object_or_404(Surah, id=id)
    serializer=SurahSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def prayer_times_api(request, region_id):
    region=get_object_or_404(Region, id=region_id).name
    url = f"https://islomapi.uz/api/present/day?region={region}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return Response(data)
    else:
        return Response({"error": "API dan ma'lumot olishda xatolik bor"}, status=500)


###################################################################

from rest_framework.views import APIView
class PrayerTime(APIView):
    def get(self, request, latitude, longitude, *args, **kwargs):
        time_difference=(longitude-69.2401)*4
        











