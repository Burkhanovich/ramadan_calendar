from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Region(models.Model):
    name =  models.CharField(unique=True)

    def __str__(self):
        return self.name

class DistrictTime(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region')
    name = models.CharField(unique=True)
    longitude=models.FloatField()
    time_difference = models.IntegerField(editable=False)


    def __str__(self):
        return self.name

class DefaultTime(models.Model):
    date=models.DateField(unique=True)
    saharlik = models.TimeField()
    iftorlik = models.TimeField()

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

class Category(models.Model):
    name=models.CharField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural='Categories'

class Surah(models.Model):
    name=models.CharField()
    description=models.TextField()
    categories = models.ManyToManyField(Category,related_name='categories')

    def __str__(self):
        return self.name



@receiver(pre_save, sender=DistrictTime)
def time_difference_pre_save(sender, instance, **kwargs):
    instance.time_difference=int(((69.2401-instance.longitude)*60)/15)





