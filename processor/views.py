from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login


# Create your views here.

def overview_week(request):
    pass


def overview_trend(request):
    pass


def farms_all(request):
    pass


def farms_report(request):
    pass


def farms_workers(request):
    pass


def farms_request(request):
    pass 


def single_farm(request,id):
    pass


def single_worker(request,id):
    pass


def single_report(request,id):
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
        print(newUser.id)
        login(request,newUser)

    return render(request,"auth-templates/login.html")


def loginFunction(request):
    
    if request.method == "POST":

        # Grab form data
        email = request.POST["email"]
        password = request.POST["passoword"]

        # Authenticate if user exists
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)

    return render(request, "auth-templates/signup.html")





        
