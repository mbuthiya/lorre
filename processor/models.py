from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Crop(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Processor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    country = models.CharField(max_length = 50,null=True)
    primary_product = models.ForeignKey(
        Crop, on_delete=models.SET_NULL, null=True)
    unit_of_measure = models.CharField(max_length=10, null=True)
    company_image = models.ImageField(
        upload_to="processor_profiles", null=True)
    
    def __str__(self):
        return self.company_name



class ExtensionWorker(models.Model):
    processor = models.ForeignKey(Processor,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    profile_image = models.ImageField(upload_to="worker_images")
    phone_number = models.IntegerField()
    started_work = models.DateField()
    gender=models.CharField(max_length=8)

    def __str__(self):
        return self.first_name


class Farm(models.Model):
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    manager = models.ForeignKey(ExtensionWorker,on_delete=models.SET_NULL,null=True)
    farmer_name = models.CharField(max_length=50)
    village_name = models.CharField(max_length=50)
    date_added = models.DateField(auto_now=True)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    farm_code = models.CharField(max_length=200)

    def __str__(self):
        return self.farmer_name

    @classmethod
    def added(cls):

        this_year = [farm for farm in cls.objects.all(
        ) if farm.date_added.year == datetime.today().year]
        number_farms_added = len(this_year)
        
        return number_farms_added
    

    @classmethod
    def search(cls,query):
        farmIds = cls.objects.filter(farm_code=query)
        location = cls.objects.filter(village_name=query)
        farmer = cls.objects.filter(farmer_name=query)

        return farmIds|location|farmer


class Season(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    estimated_yield = models.IntegerField()

    def __str__(self):
        return "Season"

    @classmethod
    def this_weeks_harvest(cls):
        this_week = datetime.isocalendar(datetime.today())[1]

        harvest = [harvest_season for harvest_season in cls.objects.all(
        ) if datetime.isocalendar(harvest_season.expected_harvest_date)[1] == this_week]

        harvestAmount = sum([amount.estimated_yield for amount in harvest])
        
        farms = [farms.farm for farms in harvest]

        return harvestAmount,farms
    

    @classmethod
    def average_yield(cls):
        harvest_yields = [harvest_season.estimated_yield for harvest_season in cls.objects.all(
        ) if harvest_season.expected_harvest_date.year == datetime.today().year]

        
        average_farm_output = sum (harvest_yields) // len(Farm.objects.all())

        return average_farm_output
