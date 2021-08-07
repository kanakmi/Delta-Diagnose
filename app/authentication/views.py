from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from twilio.rest import Client
from .models import AuthorizedDevice, TwoFAToken, TWOFAVerified
from helpers import random_str
import os


# Create your views here.
TWILIO_ACCOUNT_SID = "AC82a278d0019838fec847a68c5d0c0726"
TWILIO_AUTH_TOKEN = "950515b4422ee7915657b66b1479d7da"

c = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def register(request):
    if request.method == "POST":
        fname = request.POST['first-name']
        lname = request.POST['last-name']
        email = request.POST['email']
        country_code = request.POST['country-code']
        phone = request.POST["phone-number"]
        password = request.POST['password']

        User.objects.create_user(username=email, email=email, first_name=fname, last_name=lname, password=password).save()

        u = User.objects.get(username=email)

        code = random_str()
        c.messages.create(from_='+19162800623', body='TWOFA Code: ' + code, to='+' + country_code + phone)
        TwoFAToken(user_id=u.id, code=code, phone='+' + country_code + phone).save()

        return HttpResponse("registered successfully")

    else:
        return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse("Logged in successfully")
        else:
            return HttpResponse("Wrong credentials")

    else:
        return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return HttpResponse("Logged out successfully")