from django.db import models
from UserAuth.models import *

# Create your models here.

class DoctorSlots(models.Model):
    doc = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="DoctorSlots",null=True)
    slot_date = models.DateField(default=None,null=False,blank=True)
    slot_start_time = models.TimeField(default=None,null=False,blank=True)
    slot_end_time = models.TimeField(default=None,null=False,blank=True)
    is_booked = models.BooleanField(default=False)
    cust = models.ForeignKey(CustomUser,on_delete=models.SET_DEFAULT,related_name="CustomerSlots",null=True,default=None)

    def __str__(self):
        return str(self.doc)+" -> "+str(self.slot_date) + " -> " + str(self.slot_start_time)