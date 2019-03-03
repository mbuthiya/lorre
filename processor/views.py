from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from .models import Processor,Crop,Season,ExtensionWorker,Farm
from .charts import ThisWeekHarvest,Trend



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
        data = {}
        return render(request, "dashboard-templates/dashboard.html", {"title": "Weekly Overview", "templateName": "dashboard-templates/week-data.html", "current_processor": current_processor, "data": data})

    trend_chart = Trend(
        height=400,
        width=800,
        explicit_size=True,
    ).generate()




    data = {"trend_chart": trend_chart,"added":Farm.added(),"average_yield":Season.average_yield()}

    return render(request, "dashboard-templates/dashboard.html", {"title": "Processor Charts", "templateName": "dashboard-templates/trend.html", "current_processor": current_processor, "data": data})



@login_required
def farms_all(request):
    pass


@login_required
def farms_report(request):
    pass


@login_required
def farms_workers(request):
    pass


@login_required
def farms_request(request):
    pass


@login_required
def single_farm(request, id):
    pass


@login_required
def single_worker(request, id):
    pass


@login_required
def single_report(request, id):
    pass


def profile(request, id):

    if request.method == "POST" and request.FILES['image']:
        
        country = request.POST["cCountry"]
        unit_of_measure = request.POST["measure"]
        company_image = request.FILES["image"]
        product = request.POST["product"]

        fs = FileSystemStorage()
        filename = fs.save(company_image.name,company_image)
        try:
            primary_product=Crop.objects.get(pk=int(product))

            Processor.objects.filter(id=id).update(country=country,
                        unit_of_measure=unit_of_measure, company_image=filename,primary_product=primary_product)
            return redirect("week")
        except:
            print("Error")
    try:
         processor = Processor.objects.get(pk=id)

    except ObjectDoesNotExist:
        print("Error")
        
    products = Crop.objects.all()
    return render(request, "auth-templates/profile.html",{"processor":processor,"products":products})


def signup(request):

    if request.method == "POST":

        # Grab form data
        username = request.POST["companyName"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Add user to the database
        newUser = User.objects.create_user(username=username,email=email,password=password)
        newUser.save()

        # Create a new Processor 
        newProcessor = Processor(user=newUser,company_name=username)
        newProcessor.save()

        print(newProcessor.id)

        # Login and redirect new user
        login(request,newUser)
        return redirect("profile",newProcessor.id)
        

    return render(request,"auth-templates/signup.html")


def loginFunction(request):
    
    if request.method == "POST":

        # Grab form data
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate if user exists
        try:
            userEmail = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return redirect("signup")

        user = authenticate(request,username=userEmail.username,password=password)

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
