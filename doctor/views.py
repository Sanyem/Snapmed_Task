from django.shortcuts import render
from django.shortcuts import render,get_object_or_404, redirect
from .models import *
from UserAuth.models import *
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
def view_doc_profile(request):

    """
    Login Required 

    Function to view doctor profile

    parameters -> request(only GET request is supported for this function)

    return -> 
    
        If doctor is not authenticated then home page is rendered.

        Else profile is shown
    """

    if request.method=="GET":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            return render(request, 'doctor/view_doc_profile.html',{"user":user})


@login_required(login_url=settings.LOGIN_URL)
def edit_doc_profile(request):

    """
    Login Required

    Function to edit doctor profile

    parameters -> request

    return -> 
    
        If GET request :
            If doctor is not authenticated then home page is rendered.

            Else edit page is rendered


        If POST request:
            If doctor is not authenticated then home page is rendered.

            Else tries to edit the user details. If any exception occurs, it returns the exception as HttpResponse
    """

    if request.method=="GET":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            return render(request, 'doctor/edit_doc_profile.html',{"user":user})
    
    if request.method=="POST":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:    
                user = request.user
                user.first_name = request.POST.get("first_name")
                user.last_name = request.POST.get("last_name")
                # pic = request.FILES['pic']
                # fs = FileSystemStorage()
                # filename = fs.save(.name, myfile)
                user.pic = request.FILES.get("pic")
                user.save()
                return HttpResponseRedirect(reverse('doctor:view_doc_profile'))
            except Exception as e:
                print(e)
                return HttpResponse(e)

@login_required(login_url=settings.LOGIN_URL)
def add_slot(request,message):

    """
    Login Required

    Function to Add Slot

    parameters -> request,message

    return -> 
    
        If GET request :
            If doctor is not authenticated then home page is rendered.
            Else add slot is rendered


        If POST request:
            If doctor is not authenticated then home page is rendered.
            Else tries to add the slot details. If any exception occurs, it returns the exception as HttpResponse
    """

    if request.method=="GET":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            return render(request, 'doctor/add_slot.html',{"user":user,"message":message})

    if request.method=="POST":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            try:
                slot_date = request.POST.get("slot_date")
                slot_start_time = request.POST.get("slot_start_time")
                slot_end_time = request.POST.get("slot_end_time")
                start_time = datetime.datetime.strptime(str(slot_start_time), '%H:%M').time()
                end_time = datetime.datetime.strptime(str(slot_end_time), '%H:%M').time()
                print(start_time,end_time,slot_end_time,slot_start_time)
                # slots = DoctorSlots.objects.filter(doc=user,slot_date=slot_date,slot_start_time__range=[slot_start_time,slot_end_time],slot_end_time__range=[slot_start_time,slot_end_time]).count()
                slots = DoctorSlots.objects.filter(Q(doc=user,slot_date=slot_date,slot_start_time__range=(start_time,end_time))|Q(doc=user,slot_date=slot_date,slot_end_time__range=(start_time,end_time))).count()
                slots2 = DoctorSlots.objects.filter(doc=user,slot_date=slot_date,slot_start_time__lte=start_time,slot_end_time__gte=end_time).count()
                print(slots)
                if slots or slots2> 0:
                    return HttpResponseRedirect(reverse('doctor:add_slot', kwargs={"message":"Slot is overlapping already created slots"}))
                else:
                    doctor = DoctorSlots()
                    doctor.doc = user
                    doctor.slot_date = slot_date
                    doctor.slot_start_time = slot_start_time
                    doctor.slot_end_time = slot_end_time
                    doctor.save()
                    return HttpResponseRedirect(reverse('doctor:add_slot', kwargs={"message":"Slot created"}))
            except Exception as e:
                print(e)
                return HttpResponse(e)

@login_required(login_url=settings.LOGIN_URL)
def view_slot(request,date):
    """
    Login Required

    Function to View Slot for a particular date

    parameters -> request,date

    return -> 
    
        If GET request :
            If doctor is not authenticated then home page is rendered.
            Else for a particular date, slots are returned. If no date is mentioned then, 0 slots are returned


        If POST request:
            If doctor is not authenticated then home page is rendered.
            Else tries to post the date and redirects to the same url with date parameter. If any exception occurs, it returns the exception as HttpResponse
    """
    print(date)
    if request.method=="GET":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:
                user = request.user
                slots = DoctorSlots.objects.filter(doc=user,slot_date=date)
                slots_count = DoctorSlots.objects.filter(doc=user,slot_date=date).count()
                return render(request, 'doctor/view_slot.html',{"user":user,"date":date,"slots":slots,"count":slots_count})
            except Exception as e:
                print(e)
                return HttpResponse(e)
    
    if request.method=="POST":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            return HttpResponseRedirect(reverse('doctor:view_slot', kwargs={"date":request.POST.get("slot_date")}))


@login_required(login_url=settings.LOGIN_URL)
def edit_slot(request,id,message):

    """
    Login Required

    Function to Edit a particular Slot 

    parameters -> request, slot ID, message

    return -> 
    
        If GET request :
            If doctor is not authenticated then home page is rendered.
            Else for a particular ID, slot is returned to edit.


        If POST request:
            If doctor is not authenticated then home page is rendered.
            Else tries to post the edited details of the slot. If any exception occurs, it returns the exception as HttpResponse
    """

    print(id)
    if request.method=="GET":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:
                user = request.user
                slot = DoctorSlots.objects.get(id=id,doc=user)
                return render(request, 'doctor/edit_slot.html',{"id":id,"user":user,"slot":slot,"message":message})
            except Exception as e:
                print(e)
                return HttpResponse(e)
    
    if request.method=="POST":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            user = request.user
            try:
                slot_date = request.POST.get("slot_date")
                slot_start_time = request.POST.get("slot_start_time")
                slot_end_time = request.POST.get("slot_end_time")
                id = request.POST.get("id")
                start_time = datetime.datetime.strptime(str(slot_start_time), '%H:%M').time()
                end_time = datetime.datetime.strptime(str(slot_end_time), '%H:%M').time()
                print(start_time,end_time,slot_end_time,slot_start_time)
                # slots = DoctorSlots.objects.filter(doc=user,slot_date=slot_date,slot_start_time__range=[slot_start_time,slot_end_time],slot_end_time__range=[slot_start_time,slot_end_time]).count()
                slots = DoctorSlots.objects.filter(Q(doc=user,slot_date=slot_date,slot_start_time__range=(start_time,end_time))|Q(doc=user,slot_date=slot_date,slot_end_time__range=(start_time,end_time))&~Q(id=id)).count()
                slots2 = DoctorSlots.objects.filter(Q(doc=user,slot_date=slot_date,slot_start_time__lte=start_time,slot_end_time__gte=end_time)&~Q(id=id)).count()
                print(slots)
                if slots or slots2> 0:
                    return HttpResponseRedirect(reverse('doctor:edit_slot', kwargs={"id":id,"message":"Slot is overlapping already created slots"}))
                else:
                    doctor = DoctorSlots.objects.get(id=id,doc=user)
                    # doctor.doc = user
                    doctor.slot_date = slot_date
                    doctor.slot_start_time = slot_start_time
                    doctor.slot_end_time = slot_end_time
                    doctor.save()
                    return HttpResponseRedirect(reverse('doctor:edit_slot', kwargs={"id":id,"message":"Slot Edited"}))
            except Exception as e:
                print(e)
                return HttpResponse(e)
            # return HttpResponseRedirect(reverse('doctor:view_slot', kwargs={"date":request.POST.get("slot_date")}))


@login_required(login_url=settings.LOGIN_URL)
def delete_slot(request,id):

    """
    Login Required

    Function to Delete a particular Slot 

    parameters -> request, slot ID

    return -> 
    
        Only GET request :
            If doctor is not authenticated then home page is rendered.
            Else for a particular ID, slot is deleted and then redirected to view slot page.


    """

    if request.method=="GET":
        if not request.user.is_doctor:
            return HttpResponseRedirect(reverse('UserAuth:home'))
        else:
            try:
                user = request.user
                slot = DoctorSlots.objects.get(id=id,doc=user)
                date = slot.slot_date
                slot.delete()
                return HttpResponseRedirect(reverse('doctor:view_slot',kwargs={"date":date}))
            except Exception as e:
                print(e)
                return HttpResponse(e)
