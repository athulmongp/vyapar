from django.db import models
from django.contrib.auth.models import User

# Create by athul.
  
class company_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
   
    company_name = models.CharField(max_length=100,null=True,blank=True)
    address = models.CharField(max_length=100,null=True,blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    contact = models.CharField(max_length=100,null=True,blank=True)
    pincode = models.IntegerField(null=True,blank=True)
    pan_number = models.CharField(max_length=255,null=True,blank=True)
    dateperiod= models.CharField(max_length=255,null=True,blank=True)
    start_date = models.DateField(max_length=255,null=True,blank=True)
    End_date = models.DateField(max_length=255,null=True,blank=True)
    gst_type = models.CharField(max_length=255,null=True,blank=True)
    gst_no = models.CharField(max_length=255,null=True,blank=True)
    profile_pic = models.ImageField(null=True,blank = True,upload_to = 'image/patient')
    Action = models.IntegerField(null=True,default=0)

    # Create by athul.

class staff_details(models.Model):
    company = models.ForeignKey(company_details, on_delete=models.CASCADE,null=True,blank=True)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    user_name = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    contact = models.IntegerField(null=True,blank=True)
    img = models.ImageField(null=True,blank = True,upload_to = 'image/staff')    
    Action = models.IntegerField(null=True,default=0)

class payment_terms(models.Model):
    time_periods  = models.CharField(max_length=100,null=True,blank=True)   
  
  