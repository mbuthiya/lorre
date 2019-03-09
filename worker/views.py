from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from processor.models import ExtensionWorker,Farm,FarmAnimals,FarmPractices,FarmReport,Season
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.

# Login handler
def loginWorker(request):
    
    if request.method == "POST":
        phone_number = request.POST.get("number")
        password = request.POST.get("password")

        user = authenticate(request,username=phone_number,password=password)
        
        if user is None:
            return redirect("worker-login")
        else:
            login(request,user)
            return redirect("worker-farms")

    return render(request,"login.html")


@login_required(login_url="worker-login")
def farms(request):
    user = request.user
    
    # Get worker 
    try:
        print(user)
        manager = ExtensionWorker.objects.get(phone_number = user.username)
    except ObjectDoesNotExist:
        return Http404()
    

    # Get all the farms
    farms = Farm.objects.filter(manager=manager)
    
    
    data ={"title":"My Farms","farms":farms,"manager":manager}

    return render(request, "workerTemp/base.html", {"templateName": "workerTemp/farms.html", "data": data})



@login_required
def farm(request,id):

    user = request.user

    # Get worker
    try:
        manager = ExtensionWorker.objects.get(phone_number = user.username)
    except ObjectDoesNotExist:
        raise Http404()


    try:
        farm = Farm.objects.get(pk=id)

    except ObjectDoesNotExist:
        print("Single Farm function: Object could not be found")
        raise Http404()

    try:
        practices = FarmPractices.objects.get(farm_id=farm)
    except ObjectDoesNotExist:
        print("Single Farm function: Object could not be found")
        practices = None

    # Get all farm Animals
    animals = FarmAnimals.objects.filter(farm_id=farm)

    # Get all reports 
    reports = FarmReport.objects.filter(farm_id=farm).order_by("-report_date")

    seasons = Season.objects.filter(farm=farm)
    active_seasons = [
        active for active in seasons if active.season_active == True]

    

    data = {"animals": animals, "farm": farm, "reports": reports,
            "practice": practices, "manager": manager, "title": farm.farmer_name+"'s Farm", "seasons": active_seasons}

    return render(request, "workerTemp/base.html", {"templateName": "workerTemp/singleFarm.html", "data": data})



