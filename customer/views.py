from django.shortcuts import render
from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from UserAuth.models import *
from doctor.models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import datetime
from django.db.models import Q
# Create your views here.


@login_required(login_url=settings.LOGIN_URL)
def view_profile(request):

    """
    Login Required 

    Function to view profile

    parameters -> request(only GET request is supported for this function)

    return -> 
    
        If user is not authenticated then home page is rendered.

        Else profile is shown
    """

    if request.method=="GET":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            return render(request, 'customer/view_profile.html',{"user":user})


@login_required(login_url=settings.LOGIN_URL)
def edit_profile(request):

    """
    Login Required

    Function to edit profile

    parameters -> request

    return -> 
    
        If GET request :
            If user is not authenticated then home page is rendered.

            Else edit page is rendered


        If POST request:
            If user is not authenticated then home page is rendered.

            Else tries to edit the user details. If any exception occurs, it returns the exception as HttpResponse
    """

    if request.method=="GET":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            return render(request, 'customer/edit_profile.html',{"user":user})
    
    if request.method=="POST":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:    
                user = request.user
                user.first_name = request.POST.get("first_name")
                user.last_name = request.POST.get("last_name")
                user.pic = request.FILES.get("pic")
                user.save()
                return HttpResponseRedirect(reverse('customer:view_profile'))
            except Exception as e:
                print(e)
                return HttpResponse(e)


@login_required(login_url=settings.LOGIN_URL)
def show_doctor(request):

    """
    Login Required

    Function to show doctors

    parameters -> request

    return -> 
    
        Only GET request :
            If user is not authenticated then home page is rendered.

            Else show doctors page is rendered

    """

    if request.method=="GET":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            docs = CustomUser.objects.filter(is_doctor=True)
            docs_count = CustomUser.objects.filter(is_doctor=True).count()
            return render(request, 'customer/show_doctor.html',{"user":user,"docs":docs,"docs_count":docs_count})


@login_required(login_url=settings.LOGIN_URL)
def book_slot(request,id,date):

    """
    Login Required

    Function to choose the slot for booking

    parameters -> request, Slot id, date

    return -> 
    
        If GET request :
            If user is not authenticated then home page is rendered.

            Else gets a list of slots for a particular date and renders the html page.


        If POST request:
            If user is not authenticated then home page is rendered.

            Else tries book an available slot chosen by the user. To book a particular slot, it redirects to 'book_particular_slot' function. If any exception occurs, it returns the exception as HttpResponse
    """

    if request.method=="GET":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:
                if date is None:
                    doc = CustomUser.objects.get(id=id,is_doctor=True)
                    user = request.user
                    return render(request, 'customer/book_slot.html',{"user":user,"doc":doc})
                elif date is not None:
                    doc = CustomUser.objects.get(id=id,is_doctor=True)
                    user = request.user
                    slots = DoctorSlots.objects.filter(doc=doc,slot_date=date)
                    print(slots)
                    print(date)
                    return render(request, 'customer/book_slot.html',{"user":user,"doc":doc,"slots":slots,"slot_date":date})
            except Exception as e:
                print(e)
                return HttpResponse(e)

    if request.method=="POST":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:
                slot_date = request.POST.get("date")
                return HttpResponseRedirect(reverse('customer:book_slot', kwargs={"id":id,"date":request.POST.get("slot_date")}))
            except Exception as e:
                print(e)
                return HttpResponse(e)


@login_required(login_url=settings.LOGIN_URL)
def book_particular_slot(request,id):

    """
    Login Required

    Function to choose the slot for booking

    parameters -> request, Slot id

    return -> 
    
        If GET request :
            If user is not authenticated then home page is rendered.

            Else books a particular slot and redirects to show doctors page.

    """

    if request.method=="GET":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:    
                slot = DoctorSlots.objects.get(id=id,is_booked=False)
                user = request.user
                slot.is_booked=True
                slot.cust=user
                slot.save()
                return HttpResponseRedirect(reverse('customer:show_doctor'))
            
            except Exception as e:
                print(e)
                return HttpResponse(e)

@login_required(login_url=settings.LOGIN_URL)
def cancel_particular_slot(request,id):

    """
    Login Required

    Function to choose the slot for booking

    parameters -> request, Slot id

    return -> 
    
        If GET request :
            If user is not authenticated then home page is rendered.

            Else cancels the appointment of a particular slot and redirects to get booked slots page.

    """

    if request.method=="GET":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:    
                slot = DoctorSlots.objects.get(id=id,is_booked=True)
                user = request.user
                slot.is_booked=False
                slot.cust=None
                slot.save()
                return HttpResponseRedirect(reverse('customer:get_booked_slots'))
            
            except Exception as e:
                print(e)
                return HttpResponse(e)


@login_required(login_url=settings.LOGIN_URL)
def get_booked_slots(request,date):

    """
    Login Required

    Function to choose the slot for booking

    parameters -> request, date

    return -> 
    
        If GET request :
            If user is not authenticated then home page is rendered.

            Else shows booked slots for a particular date.

        If POST request:
            If user is not authenticated then home page is rendered.

            Else user posts a date and it redirects to itslef with a date parameter

    """


    if request.method=="GET":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:    
                if date is None:
                    user = request.user
                    return render(request, 'customer/get_booked_slots.html',{"user":user})
                elif date is not None:
                    user = request.user
                    slots = DoctorSlots.objects.filter(cust=user,slot_date=date,is_booked=True)
                    print(slots)
                    print(date)
                    today = datetime.datetime.today().strftime('%Y-%m-%d')
                    edit = False
                    if today<=date:
                        edit=True
                    print(edit)
                    return render(request, 'customer/get_booked_slots.html',{"user":user,"slots":slots,"slot_date":date,"edit":edit})
            
            except Exception as e:
                print(e)
                return HttpResponse(e)

    if request.method=="POST":
        if request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:
                slot_date = request.POST.get("date")
                return HttpResponseRedirect(reverse('customer:get_booked_slots', kwargs={"date":request.POST.get("slot_date")}))
            except Exception as e:
                print(e)
                return HttpResponse(e)

