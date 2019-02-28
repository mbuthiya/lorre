from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Crop(models.Model):
    name = models.CharField(max_length=20)


class Processor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    country = models.CharField(max_length = 50,null=True)
    primary_product = models.ForeignKey(
        Crop, on_delete=models.SET_NULL, null=True)
    unit_of_measure = models.CharField(max_length=10, null=True)
    company_image = models.ImageField(
        upload_to="processor_profiles", null=True)
    
    def __str__(self):
        return self.user


class ExtensionWorker(models.Model):
    processor = models.ForeignKey(Processor,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    profile_image = models.ImageField(upload_to="worker_images")
    phone_number = models.IntegerField(max_length=10)
    started_work = models.DateField()
    gender=models.CharField(max_length=8)

    def __str__(self):
        return self.processor


class Farm(models.Model):
    processor = models.ForeignKey(Processor, on_delete=models.CASCADE)
    manager = models.ForeignKey(ExtensionWorker,on_delete=models.SET_NULL,null=True)
    farmer_name = models.CharField(max_length=50)
    village_name = models.CharField(max_length=50)
    date_added = models.DateField(auto_now=True)
    latitude = models.CharField()
    longitude = models.CharField()
    farm_code=models.CharField()

    def __str__(self):
        return self.farmer_name


class season(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    estimated_yield = models.IntegerField()

    def __str__(self):
        return self 
    
