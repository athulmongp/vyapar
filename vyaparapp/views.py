from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.utils.text import capfirst
from django.contrib import messages
from . models import *

# Create your views here.
def home(request):
  return render(request, 'home.html')

def register_page(request):
  return render(request, 'register.html')

def register(request):
  if request.method == 'POST':
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    user_name = request.POST['uname']
    email_id = request.POST['email']
    mobile = request.POST['phone']
    passw = request.POST['password']
    c_passw = request.POST['cpassword']
    
    if passw == c_passw:
      if User.objects.filter(username = user_name).exists():
        messages.info(request, 'Sorry, Username already exists')
        return redirect('log')
      elif company_details.objects.filter(contact_number = mobile).exists():
        messages.info(request, 'Sorry, Mobile Number already exists')
        return redirect('log')

      elif not User.objects.filter(email = email_id).exists():
    
        user_data = User.objects.create_user(first_name = first_name,
                        last_name = last_name,
                        username = user_name,
                        email = email_id,
                        password = passw)
        user_data.save()
        
        data = User.objects.get(id = user_data.id)
        cust_data = company_details(contact_number = mobile,
                             user = data)
        cust_data.save()
        messages.success(request, 'Welcome'+ '' + data.first_name +' '+data.last_name + '' +'Please Login')
        return redirect('log')
      else:
        messages.info(request, 'Sorry, Email already exists')
        return redirect('log')
      
      
def login(request):
  if request.method == 'POST':
    user_name = request.POST['username']
    passw = request.POST['password']
    
    log_user = auth.authenticate(username = user_name,
                                  password = passw)
    
    if log_user is not None:
      auth.login(request, log_user)
      return redirect('homepage')
    else: 
      return redirect('log')
    
def homepage(request):
  company =  company_details.objects.get(user = request.user)
  context = {
              'company' : company
          }
  return render(request, 'homepage.html', context)

# @login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def view_profile(request):
  company =  company_details.objects.get(user = request.user)
  context = {
              'company' : company
          }
  return render(request,'profile.html',context)
  
def edit_profile(request,pk):
  company = company_details.objects.get(id = pk)
  user1 = User.objects.get(id = company.user_id)

  if request.method == "POST":

      user1.first_name = capfirst(request.POST.get('f_name'))
      user1.last_name  = capfirst(request.POST.get('l_name'))
      user1.email = request.POST.get('email')
      company.contact_number = request.POST.get('cnum')
      company.address = capfirst(request.POST.get('ards'))
      company.company_name = request.POST.get('comp_name')
      company.company_email = request.POST.get('comp_email')
      company.city = request.POST.get('city')
      company.state = request.POST.get('state')
      company.country = request.POST.get('country')
      company.pincode = request.POST.get('pinc')
      company.gst_num = request.POST.get('gst')
      company.pan_num = request.POST.get('pan')
      company.business_name = request.POST.get('bname')
      company.company_type = request.POST.get('comp_type')
      if len(request.FILES)!=0 :
          company.profile_pic = request.FILES.get('file')

      company.save()
      user1.save()
      return redirect('view_profile')

  context = {
      'company' : company,
      'user1' : user1,
  } 
  return render(request,'edit_profile.html',context)


def sale_invoices(request):
  return render(request, 'sale_invoices.html')

def estimate_quotation(request):
  return render(request, 'estimate_quotation.html')

def payment_in(request):
  return render(request, 'payment_in.html')
    
def sale_order(request):
  return render(request, 'sale_order.html')

def delivery_chellan(request):
  return render(request, 'delivery_chellan.html')

def sale_return_cr(request):
  return render(request, 'sale_return_cr.html')