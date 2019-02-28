from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def overview_week(request):
    return HttpResponse("HELLO")


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

        # Login and redirect new user
        login(request,newUser)
        return redirect("week")
        

    return render(request,"auth-templates/signup.html")


def loginFunction(request):
    
    if request.method == "POST":

        # Grab form data
        email = request.POST["email"]
        password = request.POST["passoword"]

        # Authenticate if user exists
        user = authenticate(request,email=email,password=password)
        if user is not None:
            # Login user and redirect them to week page
            login(request,user)
            return redirect("week")

    return render(request, "auth-templates/login.html")


def logoutFunction(request):
    logout(request)
    return redirect("login")
    


        
