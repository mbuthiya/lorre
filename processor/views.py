from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User


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
        print(newUser.id)
        newUser.save()

    return render(request,"auth-templates/login")

        