from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Processor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    country = models.CharField(max_length = 50,null=True)
    primary_product = models.CharField(
        Crop, null=True)
    unit_of_measure = models.CharField(max_length=10, null=True)
    company_image = models.ImageField(
        upload_to="processor_profiles", null=True)


class ExtensionWorker(models.Model):
    processor = models.ForeignKey(Processor,on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 40)
    profile_image = models.ImageField(upload_to="worker_images")
    phone_number = models.IntegerField(max_length=10)
    started_work = models.DateField()
    gender=models.CharField(max_length=8)


