from django.contrib import admin
from .models import Processor,ExtensionWorker,Farm,Crop,Season,FarmPractices,FarmAnimals,FarmCrop,FarmReport,CropManagement,CropInputs
# Register your models here.

admin.site.register(Processor)
admin.site.register(ExtensionWorker)
admin.site.register(Farm)
admin.site.register(Crop)
admin.site.register(Season)
admin.site.register(FarmPractices)
admin.site.register(FarmAnimals)
admin.site.register(FarmCrop)
admin.site.register(FarmReport)
admin.site.register(CropManagement)
admin.site.register(CropInputs)

