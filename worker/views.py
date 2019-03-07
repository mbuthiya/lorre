from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseServerError, Http404
from django.contrib.auth import authenticate



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
            print("authenticated")

    return render(request,"login.html")


