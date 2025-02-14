from rest_framework import serializers
from .models import Region, DistrictTime, DefaultTime, Category, Surah


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name', )


class DistrictTimeSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)
    class Meta:
        model = DistrictTime
        fields = ('id', 'region',  'name', 'time_difference', )

class DefaultTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultTime
        fields = ('id', 'saharlik', 'iftorlik', 'date', )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('id', 'name')


class SurahSerializer(serializers.ModelSerializer):
    categories=CategorySerializer(read_only=True, many=True)
    class Meta:
        model=Surah
        fields=('id', 'categories', 'name', 'description')

