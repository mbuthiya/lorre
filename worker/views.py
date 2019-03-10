from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseServerError, Http404, JsonResponse
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from processor.models import ExtensionWorker,Farm,FarmAnimals,FarmPractices,FarmReport,Season,FarmCrop,CropInputs,CropManagement,Crop,Requests
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


@login_required(login_url="worker-login")
def farm(request, id):

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


@login_required(login_url="worker-login")
def new_report(request,id,season):

    user = request.user

    # Get worker
    try:
        manager = ExtensionWorker.objects.get(phone_number=user.username)
    except ObjectDoesNotExist:
        print("Could not find manager")
        raise Http404()

    try:
        farm = Farm.objects.get(pk=id)

    except ObjectDoesNotExist:
        print("Single Farm function: Object could not be found")
        raise Http404()
    try:
        season = Season.objects.get(pk=season)

    except ObjectDoesNotExist:
        print("Single Season function: Object could not be found")
        raise Http404()

    try:
        reports = FarmReport.objects.get(season=season)
        return redirect("report",reports.id)

    except ObjectDoesNotExist:
        report = FarmReport.objects.create(farm_id=farm,manager=manager,season=season)
        report.save()
        return redirect("report", report.id)

   


@login_required(login_url="worker-login")
def report(request, id):

    user = request.user

    # Get worker
    try:
        manager = ExtensionWorker.objects.get(phone_number=user.username)
    except ObjectDoesNotExist:
        raise Http404()

    try:
        report = FarmReport.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404()
    
    crops = FarmCrop.objects.filter(report=report)

    cropInputs = CropInputs.objects.filter(report=report)


    cropManagement = CropManagement.objects.filter(report=report)
    
    requests = Requests.objects.filter(report=report)

    data = {"title": "Report for "+report.farm_id.farmer_name,"manager":manager,"report":report,"crops":crops,"cropInputs":cropInputs,"cropManagement":cropManagement,"requests":requests}

    return render(request, "workerTemp/base.html", {"templateName": "workerTemp/report.html", "data": data})


@login_required(login_url="worker-login")
def newComment(request, id):


    comment = request.POST.get("comment")
    try:
        report = FarmReport.objects.filter(pk=id).update(comment=comment)
    except ObjectDoesNotExist:
        raise Http404()


    data = {"success":"Added new Comment"}
    return JsonResponse(data)


@login_required(login_url="worker-login")
def new_crop_info(request, id):

    cropId = request.POST.get("crop")
    plotsize = request.POST.get("plotsize")
    intercrop= request.POST.get("inter")

    try:
        report = FarmReport.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404()


    try:
        crop = Crop.objects.get(pk = int(cropId))
    except ObjectDoesNotExist:
        raise Http404()

    cropInfo = FarmCrop.objects.create(report=report,crop=crop,inter_crop=intercrop,size= int(plotsize))

    cropInfo.save()

    data = {"success":"Successfully added new crop information"}
    return JsonResponse(data)


@login_required(login_url="worker-login")
def new_crop_manage(request, id):

    cropId = request.POST.get("crop")
    activity = request.POST.get("activity")
    status= request.POST.get("status")
    comment = request.POST.get("comment")

    try:
        report = FarmReport.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404()


    try:
        crop = Crop.objects.get(pk = int(cropId))
    except ObjectDoesNotExist:
        raise Http404()

    cropManage = CropManagement.objects.create(crop=crop,report=report,activity=activity,activity_status=status,comment=comment)
    cropManage.save()

    data = {"success":"Successfully added new Activity"}
    return JsonResponse(data)


@login_required(login_url="worker-login")
def new_crop_Input(request, id):

    product = request.POST.get("product")
    quantity= request.POST.get("quantity")
    si = request.POST.get("si")
    date = request.POST.get("date")

    try:    
        report = FarmReport.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404()
    

    cropInput = CropInputs.objects.create(report=report, product=product, product_quantity=int(quantity), product_quantity_si=si,date_of_use=date)

    cropInput.save()

    data = {"success": "Successfully added new crop input"}
    return JsonResponse(data)



@login_required(login_url="worker-login")
def new_crop_Request(request, id):

    name = request.POST.get("name")
    cost= request.POST.get("cost")
    reason = request.POST.get("reason")

    try:    
        report = FarmReport.objects.get(pk=id)
    except ObjectDoesNotExist:
        raise Http404()
    

    request = Requests.objects.create(report=report,name=name,cost=int(cost),reason=reason)
    request.save()

    request.add_to_season_investment()
    data = {"success": "Successfully added new request"}
    return JsonResponse(data)


@login_required(login_url="worker-login")
def new_season(request):

    if request.method == 'POST':
        farm = request.POST.get("farm")
        crop= request.POST.get("crop")
        planting = request.POST.get("planting")
        harvesting = request.POST.get("harvest")
        yields = request.POST.get("yield")
        price = request.POST.get("price")

        # Get worker
        try:
            
            farm_ac = Farm.objects.get(pk=int(farm))
        except ObjectDoesNotExist:
            return Http404()
        # Get worker
        try:
            
            crop_ac = Crop.objects.get(pk=int(crop))
        except ObjectDoesNotExist:
            return Http404()

        newSeason = Season.objects.create(farm=farm_ac, crop=crop_ac, planting_date=planting, expected_harvest_date=harvesting, estimated_yield=yields, price_per_unit=price)

        newSeason.save()

        return redirect("worker-farms")

    user = request.user
    
    # Get worker 
    try:
        print(user)
        manager = ExtensionWorker.objects.get(phone_number = user.username)
    except ObjectDoesNotExist:
        return Http404()
    

    # Get all the farms
    farms = Farm.objects.filter(manager=manager)
    crops = Crop.objects.all()
    
    data ={"title":"New Season","farms":farms,"manager":manager,"crops":crops}

    return render(request, "workerTemp/base.html", {"templateName": "workerTemp/newseason.html", "data": data})



