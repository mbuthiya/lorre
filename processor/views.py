from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Processor


# Create your views here.
@login_required
def overview_week(request):

    # Get the company information
    user = request.user
    current_processor = None
    try:
        current_processor = Processor.objects.get(user=user)

    except ObjectDoesNotExist:
        print("User Does Not Exist")


    return render(request, "dashboard-templates/dashboard.html", {"title": "Weekly Overview", "templateName":"dashboard-templates/week-data.html","current_processor":current_processor})


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
def single_farm(request,id):
    pass


@login_required
def single_worker(request,id):
    pass


@login_required
def single_report(request,id):
    pass


def profile(request,procesor):
    pass

def signup(request):

    if request.method == "POST":

        # Grab form data
        username = request.POST["companyName"]
        email = request.POST["email"]
        password = request.POST["password"]

        #Add user to the database
        newUser = User.objects.create_user(username=username,email=email,password=password)
        newUser.save()

        # Create a new Processor 
        newProcessor = Processor(user=newUser,company_name=username)
        newProcessor.save()

        # Login and redirect new user
        login(request,newUser)
        return redirect("profile",newProcessor)
        

    return render(request,"auth-templates/signup.html")


def loginFunction(request):
    
    if request.method == "POST":

        # Grab form data
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Authenticate if user exists
        userEmail =User.objects.get(email=email)
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
