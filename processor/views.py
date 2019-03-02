from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from .models import Processor,Crop


# Create your views here.
@login_required
def overview_week(request):

    current_processor = getUser(request)

    if current_processor == None:
        return HttpResponseServerError

    return render(request, "dashboard-templates/dashboard.html", {"title": "Weekly Overview", "templateName": "dashboard-templates/week-data.html", "current_processor": current_processor})


@login_required
def overview_trend(request):
    pass


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
    try:
        current_processor = Processor.objects.get(user=user)

    except ObjectDoesNotExist:
        print("User Does Not Exist")

    return current_processor
