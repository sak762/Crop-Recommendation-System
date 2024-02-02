from django.shortcuts import render,redirect
from django.contrib import messages
from app.auth import authentication, input_verification
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from app.models import Crop_Details
import numpy as np
import pickle
from datetime import datetime
# Create your views here.
def index(request):
    return render(request, "index.html", {'navbar' : 'home'})

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone_number = request.POST['phone_number']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(first_name, contact_no, ussername)
        verify = authentication(first_name, last_name, password, password1, phone_number)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
            # return HttpResponse("This is Home page")
    return render(request, "register.html", {'navbar' : 'register'})

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    return render(request, "log_in.html", {'navbar' : 'log_in'})

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
    }
    
    if request.method == "POST":
        farmer_name = request.POST['farmer_name']
        contact_no = request.POST['contact_no']
        n = request.POST['n']
        p = request.POST['p']
        k = request.POST['k']
        temperature = request.POST['temperature']
        humidity = request.POST['humidity']
        ph = request.POST['ph']
        rainfall = request.POST['rainfall']
        
        verify = input_verification(farmer_name, contact_no, n, p, k, temperature, humidity, ph, rainfall)
        if verify == "Success":
            with open('dataset/NBClassifier.pkl', 'rb') as f:
                NaiveBayes = pickle.load(f)
            data = np.array([[n,p,k,temperature,humidity,ph,rainfall]], dtype=float)
            pred = NaiveBayes.predict(data)
            with open('dataset/Fertilizer_Classifier.pkl', 'rb') as f:
                NaiveBayes = pickle.load(f)
            fertilizer_data = np.array([[n,p,k,temperature,humidity]], dtype=float)
            fertilizer = NaiveBayes.predict(fertilizer_data)
            message = 'Predicted Crop is : ' + pred[0]
            crop = Crop_Details(farmer_name = farmer_name, contact_no = contact_no, n = n, p = p, k = k, temperature = temperature, humidity= humidity, ph = ph, rainfall = rainfall, fertilizer = fertilizer[0])
            crop.prediction = message
            crop.date = datetime.today()
            crop.save()
            messages.info(request, message)
            return redirect("crop_report")
        else:
            messages.error(request, verify)
            return redirect("dashboard")
    return render(request, "dashboard.html", context)


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def crop_report(request):
    crop_data = Crop_Details.objects.last()
    context = {
        'first_name': request.user.first_name, 
        'last_name': request.user.last_name, 
        'crop_data' : crop_data
    }
    if request.method == "POST":
        return redirect("report")
    return render(request, "crop_report.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def report(request):
    crop_data = Crop_Details.objects.last()
    context = { 
        'crop_data' : crop_data
    }
    return render(request, "report.html", context)