from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,HttpResponseServerError,Http404
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from .models import Processor, Crop, Season, ExtensionWorker, Farm, FarmReport, FarmAnimals, FarmPractices,FarmCrop,CropInputs,CropManagement
from .charts import ThisWeekHarvest,Trend,FarmTrend




# Create your views here.
@login_required
def overview_week(request):

    current_processor,workers = getUser(request)

    if current_processor == None:
        return HttpResponseServerError
    
    if not workers:
        data ={}
        return render(request, "dashboard-templates/dashboard.html", {"title": "Weekly Overview", "templateName": "dashboard-templates/week-data.html", "current_processor": current_processor, "data": data})

    harvest_chart = ThisWeekHarvest(
        height=300,
        width=500,
    
    ).generate()
   

    harvest_amount, farms = Season.this_weeks_harvest()
    data = {"harvest_chart": harvest_chart, "harvest_amount":harvest_amount, "farms": farms}

    return render(request, "dashboard-templates/dashboard.html", {"title": "Weekly Overview", "templateName": "dashboard-templates/week-data.html", "current_processor": current_processor, "data": data})


@login_required
def overview_trend(request):

    current_processor, workers = getUser(request)
    if current_processor == None:
        return HttpResponseServerError

    if not workers:
        return redirect("week")

    trend_chart = Trend(
        height=400,
        width=800,
        explicit_size=True,
    ).generate()

    data = {"trend_chart": trend_chart,"added":Farm.added(),"average_yield":Season.average_yield()}

    return render(request, "dashboard-templates/dashboard.html", {"title": "Processor Charts", "templateName": "dashboard-templates/trend.html", "current_processor": current_processor, "data": data})



@login_required
def farms_all(request):
    current_processor, workers = getUser(request)
    if current_processor == None:
        return HttpResponseServerError

    if not workers:
       return redirect("week")

    if request.GET:
        all_farms = Farm.search(request.GET["farm-search"])
        data = {"all_farms": all_farms,
                "search_param": request.GET["farm-search"]}
    else:
        all_farms = Farm.objects.all()
        data = {"all_farms":all_farms}

    return render(request, "dashboard-templates/dashboard.html", {"title": "All Farms", "templateName": "dashboard-templates/farms.html", "current_processor": current_processor, "data": data})



@login_required
def new_farms(request):

    current_processor, workers = getUser(request)
    if current_processor == None:
        return HttpResponseServerError()

    if not workers:
       return redirect("week")

    # Add form input
    if request.method == "POST":
        farmer = request.POST.get("farmer")
        manager = request.POST.get("manager")
        village = request.POST.get("village")
        longitude = request.POST.get("longitude")
        latitude = request.POST.get("latitude")
        farm_code = request.POST.get("code")
        farm_size = request.POST.get("farm_size")
        date = request.POST.get("date")

        manager = ExtensionWorker.objects.get(pk=int(manager))

        new_farm = Farm.objects.create(processor=current_processor, farmer_name=farmer, manager=manager,
                                       village_name=village, longitude=longitude, latitude=latitude, farm_code=farm_code, farm_size_ha=int(farm_size),
                                       date_added=date)

        new_farm.save()
        return redirect("farms")

    managers = ExtensionWorker.objects.filter(processor=current_processor)

    data={"managers":managers}
    return render(request, "dashboard-templates/dashboard.html", {"title": "All Farms", "templateName": "dashboard-templates/newFarm.html", "current_processor": current_processor, "data": data})


@login_required
def farms_workers(request):
    current_processor, workers = getUser(request)
    if current_processor == None:
        return HttpResponseServerError()

    if not workers:
       return redirect("week")
    if request.GET:
        workers = ExtensionWorker.findWorker(request.GET["worker-search"])
        data = {"workers": workers,
                "search_param": request.GET["worker-search"]}
    else:
        workers = ExtensionWorker.objects.all()
        data = {"workers":workers}

    return render(request, "dashboard-templates/dashboard.html", {"title": "All Farms", "templateName": "dashboard-templates/workers.html", "current_processor": current_processor, "data": data})




@login_required
def new_worker(request):

    current_processor, workers = getUser(request)

    if current_processor == None:
        return HttpResponseServerError()

    if request.method == "POST" and request.FILES['image']:

        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        gender = request.POST["gender"]
        profile_image = request.FILES["image"]
        phone_number = request.POST["number"]

        fs = FileSystemStorage()
        filename = fs.save(profile_image.name, profile_image)

        # Creating a new user instance
        newuser = User.objects.create_user(username=phone_number,password="12345678")
        newuser.save()

        # Creating a new extension worker
        ext=ExtensionWorker.objects.create(processor=current_processor, first_name=first_name,last_name=last_name,gender=gender,profile_image=filename,phone_number=phone_number)
        ext.save()

        return redirect("workers")
    # End of post
    data={}
    return render(request, "dashboard-templates/dashboard.html", {"title": "New Worker", "templateName": "dashboard-templates/newWorker.html", "current_processor": current_processor, "data": data})
    


@login_required
def single_farm(request, id):

    current_processor, workers = getUser(request)
    if current_processor == None:
        return HttpResponseServerError()

    if not workers:
       return redirect("week")
    
    # Check if farm exists
    farm = ""
    try:
        farm = Farm.objects.get(pk=id)

    except ObjectDoesNotExist:
        print("Single Farm function: Object could not be found")
        raise Http404()
    
    # Get farm information
    # Sum of yeild from this and previous season
    status,percentage = Season.get_farm_yield(farm)
    
   
    # Get chart
    farm_chart = FarmTrend(
        height=300,
        width=500,
        explicit_size=True,
    ).generate(farm)

    try:
        practices = FarmPractices.objects.get(farm_id=farm)
    except ObjectDoesNotExist:
        print("Single Farm function: Object could not be found")
        practices=None


    
    # Get all farm Animals
    animals = FarmAnimals.objects.filter(farm_id =farm)

    # Get all reports
    reports = FarmReport.objects.filter(farm_id=farm).order_by("-report_date")
    
    data={"status":status,"percentage":percentage,"farm_trend":farm_chart,"animals":animals,"farm":farm,"reports":reports,"practice":practices}
    
    return render(request, "dashboard-templates/dashboard.html", {"title": "Farm", "templateName": "dashboard-templates/farm.html", "current_processor": current_processor, "data": data})
    



@login_required
def single_report(request, id):

    current_processor, workers = getUser(request)
    if current_processor == None:
        return HttpResponseServerError()

    if not workers:
       return redirect("week")
    
    # Check if the report exists
    try:
        report = FarmReport.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Http404()
    
    crops = FarmCrop.objects.filter(report = report)

    cropInputs = CropInputs.objects.filter(report=report)

    cropManagement = CropManagement.objects.filter(report=report)
    
    data = {"report":report,"crops":crops,"cropInputs":cropInputs,"cropManagement":cropManagement}

    return render(request, "dashboard-templates/dashboard.html", {"title": "Farm", "templateName": "dashboard-templates/report.html", "current_processor": current_processor, "data": data})


@login_required
def profile(request, id):

    if request.method == "POST" and request.FILES['image']:
        
        country = request.POST["cCountry"]
        company_image = request.FILES["image"]
        

        fs = FileSystemStorage()
        filename = fs.save(company_image.name,company_image)

        try:
            Processor.objects.filter(id=id).update(country=country, company_image=filename,)
            return redirect("week")
        except:
            print("Error")
    try:
         processor = Processor.objects.get(pk=id)

    except ObjectDoesNotExist:
        print("Error")
        
    return render(request, "auth-templates/profile.html",{"processor":processor})


@login_required
def newCrop(request):

    if request.method =="POST":
        name = request.POST.get("name")
        unit_of_measure = request.POST.get("measure")

        newCrop = Crop.objects.create(name=name,unit_of_measure=unit_of_measure)
        newCrop.save()
    else:
        return redirect("week")
    

def signup(request):

    if request.method == "POST":

        # Grab form data
        username = request.POST["companyName"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Add user to the database
        newUser = User.objects.create_user(username=email,email=email,password=password)
        newUser.save()

        # Create a new Processor 
        newProcessor = Processor(user=newUser,company_name=username)
        newProcessor.save()

        # Login and redirect new user
        login(request,newUser)
        return redirect("profile",newProcessor.id)
        

    return render(request,"auth-templates/signup.html")


def loginFunction(request):
    
    if request.method == "POST":

        # Grab form data
        email = request.POST.get("email")
        password = request.POST.get("password")


        user = authenticate(request,username=email,password=password)

        if user is not None:
            # Login user and redirect them to week page
            login(request,user)
            return redirect("week")
        else:
            return redirect("signup")



    return render(request, "auth-templates/login.html")


def logoutFunction(request):
    logout(request)
    return redirect("login")


def getUser(request):
    # Get the company information
    user = request.user
    current_processor = None
    has_workers = False

    try:
        current_processor = Processor.objects.get(user=user)
       
    except ObjectDoesNotExist:
        print("User Does Not Exist")
    
    workers = [workers for workers in ExtensionWorker.objects.filter(processor=current_processor)]

    if len(workers) > 0:
        has_workers =True


    return current_processor,has_workers
