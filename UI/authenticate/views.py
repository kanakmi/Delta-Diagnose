from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import random
from userdata.models import sendotp,profile

def signup(request):
    if request.user.is_authenticated:
        return redirect('/Get-file')
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            data = profile()
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            user1 = form.save()
            data.user = user1
            data.first_name = fname
            data.last_name = lname
            data.email = email
            data.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            print(fname,lname,email,user,password)
            login(request,user)
            sendOtp(str(fname+" "+lname),email,user1)
            return redirect('verify')
        else:
            return render(request, 'signup.html',{'form':form})
    else:
        form = UserCreationForm()
        return render(request, 'signup.html',{'form':form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('/Get-file')
    if request.method =='POST':
        username = request.POST['username']
        password1 = request.POST['password']
        user = authenticate(request, username = username, password = password1)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            form = AuthenticationForm(request.POST)
            return render(request,'signin.html',{'form':form})
    else:
        form = AuthenticationForm()
        return render(request,'signin.html',{'form':form})


def signout(request):
    logout(request)
    return redirect('/')

def sendOtp(name,email,user1):    
    subject = 'Verification Code'
    otp = str(random.randrange(100000,999999))
    message = 'Welcome  '+name+'\n\n OTP for Delta Diagnose is-  '+ otp
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]    
    send_mail( subject, message, email_from, recipient_list )
    data = sendotp()
    data.user = user1
    data.otp = otp
    data.save()

def check(user1):
    try:
        sendotp.objects.get(user = user1)
        return True
    except:
        return False

def verify(request):
    user1 = request.user
    try:
        data = sendotp.objects.get(user = user1)
        otp = request.POST.get('otp')
        if request.method=='POST':
            if(otp==data.otp):
                data.delete()
                return redirect('index')      
    except:
        return redirect('index')
    return render(request,'verify.html')