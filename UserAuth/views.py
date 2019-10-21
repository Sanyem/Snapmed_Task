from django.shortcuts import render
from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from doctor.models import *
from customer.models import *
# Create your views here.



def logout(request):
    """
    Function for logout

    parameters -> request(only GET request is supported for this function)
    
    return -> URL redirect to home page using HttpResponseRedirect
    
    After logging in, the logout button will appear in the navbar. 
    """
    if request.method=="GET":
        if request.user.is_authenticated:
            auth.logout(request)
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            return HttpResponseRedirect(reverse('UserAuth:home'))

def home(request):
    """
    Function to render the home page

    parameters -> request(only GET request is supported for this function)

    return -> If no user is authenticated then home page is rendered. If a user or a doctor is already authenticated, then it redirects to the profile page of the user
    """
    if request.method=="GET":
        if request.user.is_authenticated and request.user.is_doctor:
            return HttpResponseRedirect(reverse('doctor:view_doc_profile'))
        elif request.user.is_authenticated and not request.user.is_doctor:
            return HttpResponseRedirect(reverse('customer:view_profile'))
        return render(request, 'UserAuth/home.html')

def doc_signup(request,message):
    
    """
    Function to render the home page

    parameters -> request,message

    return -> 
        if GET request --> If no user is authenticated then signup page is rendered. If a user or a doctor is already authenticated, then it redirects to the profile page of the user

        if POST request --> Checks if email already exists, check if passwords match, then tries to signup the doctor. If an exception occurs, then it returns an exception. 
    """

    if request.method=="GET":
        if request.user.is_authenticated and request.user.is_doctor==False:
            return HttpResponseRedirect(reverse('customer:view_profile'))
        if request.user.is_authenticated and request.user.is_doctor==True:
            return HttpResponseRedirect(reverse('doctor:view_doc_profile'))
        return render(request, 'UserAuth/doc_signup.html',{"message":message})
    
    if request.method=="POST":
        if CustomUser.objects.filter(username=request.POST.get('email')).count():
            return HttpResponseRedirect(reverse('UserAuth:doc_signup', kwargs={"message":"Email already exists. Please choose some other email"}))
        # elif CustomUser.objects.filter(email=request.POST.get('email')).count():
        #     return HttpResponse("User Already registered with the given email")
        else:
            if request.POST.get('password')!=request.POST.get('confirm_password'):
                return HttpResponseRedirect(reverse('UserAuth:doc_signup', kwargs={"message":"Passwords don't match"}))
            else:
                try:
                    doc = CustomUser()
                    doc.first_name = request.POST.get('first_name')
                    doc.last_name = request.POST.get('last_name')
                    doc.is_doctor = True
                    doc.username = request.POST.get('email')
                    doc.email = request.POST.get('email')
                    doc.set_password(request.POST.get('password'))
                    doc.save()
                    return HttpResponseRedirect(reverse('UserAuth:doc_login', kwargs={"message":''}))
                except Exception as e:
                    print(e)
                    mes = "An Exception Occured ->" + str(e)
                    return HttpResponseRedirect(reverse('UserAuth:doc_signup', kwargs={"message":mes}))

def doc_login(request,message):

    """
    Function to render the home page

    parameters -> request,message

    return -> 
        if GET request --> If no user is authenticated then login page is rendered. If a user or a doctor is already authenticated, then it redirects to the profile page of the user

        if POST request --> Tries to login the doctor. If an exception occurs, then it returns an exception. 
    """

    if request.method=="GET":
        if request.user.is_authenticated and request.user.is_doctor==False:
            return HttpResponseRedirect(reverse('customer:view_profile'))
        if request.user.is_authenticated and request.user.is_doctor==True:
            return HttpResponseRedirect(reverse('doctor:view_doc_profile'))
        return render(request, 'UserAuth/doc_login.html',{"message":message})

    if request.method=="POST":
        login_username = request.POST.get('email')
        login_password = request.POST.get('password')
        try:
            doc = get_object_or_404(CustomUser,username=login_username)
            if doc.is_doctor:
                user = authenticate(username=login_username,password=login_password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect(reverse('doctor:view_doc_profile'))
            else:
                return HttpResponseRedirect(reverse('UserAuth:doc_login', kwargs={"message":"User is not a Doctor"}))
        except Exception as e:
            print(e)
            return HttpResponse(e)
        

def user_signup(request,message):

    """
    Function to render the home page

    parameters -> request,message

    return -> 
        if GET request --> If no user is authenticated then signup page is rendered. If a user or a doctor is already authenticated, then it redirects to the profile page of the user

        if POST request --> Checks if email already exists, check if passwords match, then tries to signup the user. If an exception occurs, then it returns an exception. 
    """

    if request.method=="GET":
        if request.user.is_authenticated and request.user.is_doctor==False:
            return HttpResponseRedirect(reverse('customer:view_profile'))
        if request.user.is_authenticated and request.user.is_doctor==True:
            return HttpResponseRedirect(reverse('doctor:view_doc_profile'))
        return render(request, 'UserAuth/user_signup.html',{"message":message})
    
    if request.method=="POST":
        if CustomUser.objects.filter(username=request.POST.get('email')).count():
            return HttpResponseRedirect(reverse('UserAuth:user_signup', kwargs={"message":"Email already exists. Please choose some other email"}))
        # elif CustomUser.objects.filter(email=request.POST.get('email')).count():
        #     return HttpResponse("User Already registered with the given email")
        else:
            if request.POST.get('password')!=request.POST.get('confirm_password'):
                return HttpResponseRedirect(reverse('UserAuth:user_signup', kwargs={"message":"Passwords dont match"}))
            else:
                try:
                    user = CustomUser()
                    user.first_name = request.POST.get('first_name')
                    user.last_name = request.POST.get('last_name')
                    user.is_doctor = False
                    user.username = request.POST.get('email')
                    user.email = request.POST.get('email')
                    user.set_password(request.POST.get('password'))
                    user.save()
                    return HttpResponseRedirect(reverse('UserAuth:user_login', kwargs={"message":''}))
                except Exception as e:
                    print(e)
                    mes = "An Exception Occured ->" + str(e)
                    return HttpResponseRedirect(reverse('UserAuth:user_signup', kwargs={"message":mes}))


def user_login(request,message):

    """
    Function to render the home page

    parameters -> request,message

    return -> 
        if GET request --> If no user is authenticated then login page is rendered. If a user or a doctor is already authenticated, then it redirects to the profile page of the user

        if POST request --> Tries to login the user. If an exception occurs, then it returns an exception. 
    """
    
    if request.method=="GET":
        if request.user.is_authenticated and request.user.is_doctor==False:
            return HttpResponseRedirect(reverse('customer:view_profile'))
        if request.user.is_authenticated and request.user.is_doctor==True:
            return HttpResponseRedirect(reverse('doctor:view_doc_profile'))
        return render(request, 'UserAuth/user_login.html',{"message":message})

    if request.method=="POST":
        login_username = request.POST.get('email')
        login_password = request.POST.get('password')
        try:
            doc = get_object_or_404(CustomUser,username=login_username)
            if not doc.is_doctor:
                user = authenticate(username=login_username,password=login_password)
                if user is not None:
                    login(request,user)
                    return HttpResponseRedirect(reverse('customer:view_profile'))
            else:
                return HttpResponseRedirect(reverse('UserAuth:user_login', kwargs={"message":"User is not a Customer"}))
        except Exception as e:
            print(e)
            return HttpResponse(e)