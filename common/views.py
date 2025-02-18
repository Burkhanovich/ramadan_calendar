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
    qs=DistrictTime.objects.all().filter(region__id=pk)
    serializer=DistrictTimeSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ramadan_time(request, d_id):
    obj = get_object_or_404(DistrictTime, id=d_id)
    default_times = DefaultTime.objects.all()
    time_difference = timedelta(minutes=obj.time_difference)
    data={
        'region':obj.region.name,
        'district':obj.name
    }
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
def category_detail(request, pk):
    obj=get_object_or_404(Category, id=pk)
    serializer=CategorySerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', ])
def surah_list(request):
    qs=Surah.objects.all()
    serializer=SurahSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', ])
def surah_detail(request, pk):
    obj=get_object_or_404(Surah, id=pk)
    serializer=SurahSerializer(obj)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def prayer_times_api_by_region(request, region_id):
    region=get_object_or_404(Region, id=region_id).name
    url = f"https://islomapi.uz/api/present/day?region={region}"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        return Response(data)
    else:
        return Response({"error": "API dan ma'lumot olishda xatolik bor"}, status=500)


@api_view(['GET'])
def prayer_times_api_by_district(request, district_id):
    obj = get_object_or_404(DistrictTime, id=district_id)
    url = f"https://islomapi.uz/api/present/day?region=Toshkent"
    response = requests.get(url)
    if response.status_code != 200:
        return Response({"error": "API dan ma'lumot olishda xatolik bor"}, status=500)
    api_data = response.json()
    time_difference = timedelta(minutes=obj.time_difference)

    bomdod_time = datetime.strptime(api_data['times']['tong_saharlik'], "%H:%M").time()
    quyosh_time = datetime.strptime(api_data['times']['quyosh'], "%H:%M").time()
    peshin_time = datetime.strptime(api_data['times']['peshin'], "%H:%M").time()
    asr_time = datetime.strptime(api_data['times']['asr'], "%H:%M").time()
    shom_time = datetime.strptime(api_data['times']['shom_iftor'], "%H:%M").time()
    hufton_time = datetime.strptime(api_data['times']['hufton'], "%H:%M").time()

    bomdod = (datetime.combine(datetime.today(), bomdod_time) + time_difference).time()
    quyosh = (datetime.combine(datetime.today(), quyosh_time) + time_difference).time()
    peshin = (datetime.combine(datetime.today(), peshin_time) + time_difference).time()
    asr = (datetime.combine(datetime.today(), asr_time) + time_difference).time()
    shom = (datetime.combine(datetime.today(), shom_time) + time_difference).time()
    hufton = (datetime.combine(datetime.today(), hufton_time) + time_difference).time()

    data = {
        'region': obj.region.name,
        'district': obj.name,
        'bomdod': bomdod.strftime('%H:%M'),
        'quyosh': quyosh.strftime("%H:%M"),
        'peshin': peshin.strftime("%H:%M"),
        'asr': asr.strftime("%H:%M"),
        'shom': shom.strftime("%H:%M"),
        'hufton': hufton.strftime("%H:%M"),
    }

    return Response(data, status=200)


@api_view(["GET"])
def today_ramadan_times(request, district_id):
    time = get_object_or_404(DefaultTime, date=datetime.today().date())
    district = get_object_or_404(DistrictTime, id=district_id)
    time_difference = timedelta(minutes=district.time_difference)
    saharlik = (datetime.combine(time.date, time.saharlik) + time_difference).time()
    iftorlik = (datetime.combine(time.date, time.iftorlik) + time_difference).time()
    data = {
        'region': district.region.name,
        'district': district.name,
        'saharlik': saharlik.strftime('%H:%M'),  # String format
        'iftorlik': iftorlik.strftime('%H:%M')   # String format
    }
    return Response(data, status=status.HTTP_200_OK)




###################################################################






