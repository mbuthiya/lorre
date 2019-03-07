from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from processor.models import ExtensionWorker,Farm
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.

# Login handler
def login(request):
    
    if request.method == "POST":
        phone_number = request.POST.get("number")
        password = request.POST.get("password")

        user = authenticate(request,username=phone_number,password=password)
        
        if user is None:
            return redirect("worker-login")
        else:
            return redirect("worker-farms")

    return render(request,"login.html")



@login_required(login_url="/manager/")
def farms(request):
    user = request.user

    # Get worker 
    try:
         manager = ExtensionWorker.objects.get(phone_number = user.username)
    except ObjectDoesNotExist:
        return Http404()
    

    # Get all the farms
    farms = Farm.objects.filter(manager=manager)
    
    data ={"title":"My Farms","farms":farms,"manager":manager}

    return render(request,"workerTemp/base.html",{"data":data})




