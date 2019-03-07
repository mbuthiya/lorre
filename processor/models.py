from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.


class Crop(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Processor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, null=True)
    primary_product = models.ForeignKey(
        Crop, on_delete=models.SET_NULL, null=True)
    unit_of_measure = models.CharField(max_length=10, null=True)
    company_image = models.ImageField(upload_to="processors", null=True)

    def __str__(self):
        return self.company_name


class ExtensionWorker(models.Model):
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    profile_image = models.ImageField(upload_to="workers", null=True)
    phone_number = models.CharField(max_length=15,unique=True)
    started_work = models.DateField(auto_now=True)
    gender = models.CharField(max_length=8)

    def __str__(self):
        return self.first_name

    @classmethod
    def findWorker(cls, search):
        workers = cls.objects.filter(first_name=search)
        return workers


class Farm(models.Model):
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        ExtensionWorker, on_delete=models.SET_NULL, null=True)
    farmer_name = models.CharField(max_length=50)
    village_name = models.CharField(max_length=50)
    date_added = models.DateField()
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    farm_code = models.CharField(max_length=200)
    farm_size_ha = models.IntegerField()
    is_organic = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.farmer_name

    @classmethod
    def added(cls):

        this_year = [farm for farm in cls.objects.all(
        ) if farm.date_added.year == datetime.today().year]
        number_farms_added = len(this_year)

        return number_farms_added

    @classmethod
    def search(cls, query):
        farmIds = cls.objects.filter(farm_code=query)
        location = cls.objects.filter(village_name=query)
        farmer = cls.objects.filter(farmer_name=query)

        return farmIds | location | farmer


class Season(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    estimated_yield = models.IntegerField()
    season_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.planting_date)

    @classmethod
    def this_weeks_harvest(cls):
        this_week = datetime.isocalendar(datetime.today())[1]

        harvest = [harvest_season for harvest_season in cls.objects.all(
        ) if datetime.isocalendar(harvest_season.expected_harvest_date)[1] == this_week]

        harvestAmount = sum([amount.estimated_yield for amount in harvest])

        farms = [farms.farm for farms in harvest]

        return harvestAmount, farms

    @classmethod
    def average_yield(cls):
        harvest_yields = [harvest_season.estimated_yield for harvest_season in cls.objects.all(
        ) if harvest_season.expected_harvest_date.year == datetime.today().year]

        average_farm_output = sum(harvest_yields) // len(Farm.objects.all())

        return average_farm_output
    

    @classmethod
    def get_farm_yield(cls,farm):
        seasons = cls.objects.filter(farm=farm)

        this_year_yield = sum([yields.estimated_yield for yields in seasons if yields.expected_harvest_date.year==datetime.today().year])
        last_year_yield = sum([yields.estimated_yield for yields in seasons if yields.expected_harvest_date.year==datetime.today().year-1])

        if this_year_yield >= last_year_yield:
            status = "Increase"
        else:
            status = "Decrease"
        
        percentage = (max(this_year_yield,last_year_yield) - min(this_year_yield,last_year_yield)) // max(this_year_yield,last_year_yield) *100

        return status,percentage


class FarmPractices(models.Model):
    farm_id = models.ForeignKey(Farm,on_delete=models.CASCADE)
    flood_irrigation= models.BooleanField(default=False)
    sprinkler_irrigation= models.BooleanField(default=False)
    drip_irrigation= models.BooleanField(default=False)
    natural_enemies= models.BooleanField(default=False)
    animal_manure = models.BooleanField(default=False)
    green_manure = models.BooleanField(default=False)
    compost_used_per_ha = models.BooleanField(default=False)
    animal_manure_quantity = models.IntegerField(null=True)
    compost_used_quantity = models.IntegerField(null=True)
    manua_weeding = models.BooleanField(default=False)

    def __str__(self):
        return "Farm Practice"


class FarmAnimals(models.Model):
    farm_id = models.ForeignKey(Farm, on_delete=models.CASCADE)
    animal_name = models.CharField(max_length=50)
    number_of_animals = models.IntegerField()
    percentage_as_manure = models.IntegerField()

    def __str__(self):
        return self.animal_name


class FarmReport(models.Model):
    farm_id = models.ForeignKey(Farm, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now=True)
    manager = models.ForeignKey(ExtensionWorker, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField(default=True)
    comment = models.TextField()

    def __str__(self):
        return str(self.report_date)


class FarmCrop(models.Model):
    report = models.ForeignKey(FarmReport, on_delete=models.SET_NULL, null=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True)
    inter_crop = models.CharField(max_length=100)
    size = models.IntegerField(null=True)

    def __str__(self):
        return "Farm Crop"


class CropManagement(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True)
    report = models.ForeignKey(FarmReport, on_delete=models.CASCADE, null=True)
    activity = models.CharField(max_length=400)
    activity_status = models.CharField(max_length=300)
    comment = models.TextField()

    def __str__(self):
        return self.crop.name


class CropInputs(models.Model):
    report = models.ForeignKey(
        FarmReport, on_delete=models.SET_NULL, null=True)
    product = models.CharField(max_length=100)
    product_quantity = models.IntegerField()
    product_quantity_si = models.CharField(max_length=10)
    date_of_use = models.DateField()

    def __str__(self):
        return self.product


