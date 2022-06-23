from http.client import HTTPResponse
from django.shortcuts import redirect , render 
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout
from mist import settings
from django.core.mail import send_mail
# Create your views here.
def home(request):
    return render(request,"hospital/index.html")

def signup(request):
    if request.method=="POST":
        username=request.POST["username"]
        fname=request.POST["fname"]
        lname=request.POST["lname"]
        email_id=request.POST["email id"]
        password=request.POST["password"]
        cpassword=request.POST["cpassword"]

        if User.objects.filter(username=username):
            messages.error(request,"username already exist")
            return redirect("home")
        if User.objects.filter(email=email_id):
            messages.error(request,"email already have account")
            return redirect("home")
        
        if len(username)<10:
            messages.error(request,"username must be under 10 character")

        if password !=cpassword:
            messages.error(request,"password does not match")

        if not username.isalnum():
            messages.error(request,"username must have alpha_numerical")
            return redirect("home")



        myuser=User.objects.create_user(username,email_id,password)
        myuser.first_name = fname
        myuser.last_name=lname

        myuser.save() 

        messages.success(request,"Your Account Successfuly created")

        # welcome email
        subject="welcome to hospital - django login"
        message="hello" + myuser.first_name + "!! \n" +  "welcome to hospital \n thanks for visiting our website\n we also have sent you a confirmation email ,please confirm in order to activate your account. \n\n Thankyou "
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email, to_list, fail_silent=True)




        return redirect("signin")

    return render(request,"hospital/signup.html")
def signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["Password"]
       

        user= authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,"hospital/dashboard.html",{"fname":fname})
        
        else:
            messages.error(request,"Bad credentials!")
            return redirect("home")
    
    
    return render(request,"hospital/signin.html")
    
    
def dashboard(request):
    return render(request,"hospital/dashboard.html")



def signout(request):
    logout(request)
    return redirect("home")
