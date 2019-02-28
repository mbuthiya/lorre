from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Processor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    country = models.CharField(max_length = 50,null=True )
    primary_product = models.OneToOneField(
        Crop, on_delete=models.CASCADE, null=True)
    unit_of_measure = models.CharField(max_length=10, null=True)
    company_image = models.ImageField(
        upload_to="Processor_Profiles", null=True)
