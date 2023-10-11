from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.utils.text import capfirst
from django.contrib import messages
from . models import *
import json
from django.http.response import JsonResponse

# Create your views here.
def home(request):
  return render(request, 'home.html')



    
def homepage(request):
  company =  company_details.objects.get(user = request.user)
  context = {
              'company' : company
          }
  return render(request, 'company/homepage.html', context)

def staffhome(request,id):
  staff =  staff_details.objects.get(id=id)
  context = {
              'staff' : staff
          }
  return render(request, 'staff/staffhome.html', context)
def adminhome(request):
 
  
  
  return render(request, 'admin/adminhome.html')




# @login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def view_profile(request):
  company =  company_details.objects.get(user = request.user) 
  selected_options = request.session.get('selected_options', None)
  
  context = {
              'company' : company,
              'selected_options': json.dumps(selected_options)
          }
  return render(request,'profile.html',context)
  
def edit_profile(request,pk):
  company = company_details.objects.get(id = pk)
  user1 = User.objects.get(id = company.user_id)
  selected_options = request.session.get('selected_options', None)

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
      'selected_options': json.dumps(selected_options)
  } 
  return render(request,'company/edit_profile.html',context)


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


# created by athul
def settings(request):
  company =  company_details.objects.get(user = request.user)
  selected_options = request.session.get('selected_options', None)
  
  context = {
              'company' : company,
              'selected_options': json.dumps(selected_options),
              
          }
  return render(request, 'company/settings.html',context)

def hide_options(request):
    
    company =  company_details.objects.get(user = request.user)
    if request.method == 'POST':
        selected_options = list(request.POST.getlist('selected_options'))

    request.session['selected_options'] = selected_options
    
    context = {'selected_options': json.dumps(selected_options),
               'company' : company}
   
    return render(request, 'company/homepage.html', context)

# ------created by athul------

def company_reg(request):
  return render(request,'company/register.html')

def register(request):
  if request.method == 'POST':
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    user_name = request.POST['uname']
    email_id = request.POST['eid']
    mobile = request.POST['ph']
    passw = request.POST['pass']
    c_passw = request.POST['cpass']
    
    if passw == c_passw:
      if User.objects.filter(username = user_name).exists():
        messages.info(request, 'Sorry, Username already exists')
        return redirect('company_reg')
      

      elif not User.objects.filter(email = email_id).exists():
    
        user_data = User.objects.create_user(first_name = first_name,
                        last_name = last_name,
                        username = user_name,
                        email = email_id,
                        password = passw)
        user_data.save()
        
        data = User.objects.get(id = user_data.id)
        cust_data = company_details( contact=mobile,
                             user = data)
        cust_data.save()
        messages.success(request, 'Welcome'+ ' ' +  data.first_name +' '+data.last_name + ' '+ 'Please Login')
        return redirect('company_reg2')
      else:
        messages.info(request, 'Sorry, Email already exists')
        return redirect('company_reg')
    return render(request,'company/register.html')  
def company_reg2(request):
  
  return render(request,'company/register2.html')  
def add_company(request):
  
  print(id)
  if request.method == 'POST':
    email=request.POST['email']
    user=User.objects.get(email=email)
    company = company_details.objects.get(user = user)
    company.company_name=request.POST['cname']

    company.address=request.POST['address']
    company.city=request.POST['city']
    company.state=request.POST['state']
    company.country=request.POST['country']
    company.pincode=request.POST['pincode']
    company.pan_number=request.POST['pannumber']
    company.gst_type=request.POST['gsttype']
    company.gst_no=request.POST['gstno']
    company.profile_pic=request.FILES.get('image')
    company.dateperiod=request.POST['select']
    company.End_date=request.POST['end']
   
    company.save()

    return redirect('home')  
  return render(request,'company/register2.html')   

def staff_register(request):
  company=company_details.objects.all()

  return render(request, 'staff/staffreg.html',{'company':company})

def staff_registraction(request):
  if request.method == 'POST':
    fn=request.POST['fname']
    ln=request.POST['lname']
    email=request.POST['eid']
    un=request.POST['uname']
    pas=request.POST['pass']
    ph=request.POST['ph']
    cid=request.POST['select']
    company=company_details.objects.get(id=cid)
    img=request.FILES.get('image')

    if staff_details.objects.filter(user_name=un).exists():
      print("1")
      return redirect('staff_register')
    elif staff_details.objects.filter(email=email).exists():
      print("2")
      return redirect('staff_register')
    else:
      
      staff=staff_details(first_name=fn,last_name=ln,email=email,user_name=un,password=pas,contact=ph,img=img,company=company)
      staff.save()
      print("success")
      return redirect('log_page')

  else:
    print(" error")
    return redirect('staff_register')
  
def log_page(request):
  return render(request, 'log.html')
  
def login(request):
  if request.method == 'POST':
    user_name = request.POST['username']
    passw = request.POST['password']
    
    log_user = auth.authenticate(username = user_name,
                                  password = passw)
    
    if log_user is not None:
      auth.login(request, log_user)
      if request.user.is_staff==1:
        return redirect('adminhome')
      else:
        data=company_details.objects.get(user=request.user)
        if data.Action == 1:
          return redirect('homepage')
        else:
          messages.info(request, 'Approval is Pending..')
          return redirect('log_page')

    elif staff_details.objects.filter(user_name=user_name,password=passw).exists(): 
      data=staff_details.objects.get(user_name=user_name,password=passw)
      if data.Action == 1:
        return redirect('staffhome',data.id)  
      else:
        messages.info(request, 'Approval is Pending..')
        return redirect('log_page')

    else:
      messages.info(request, 'Invalid Username or Password. Try Again.')
      return redirect('log_page')
def adminaccept(request,id):
  data=company_details.objects.filter(id=id).update(Action=1)
  return redirect('adminhome')
def adminreject(request,id):
  data=company_details.objects.get(id=id)
  data.user.delete()
  data.delete()
  return redirect('adminhome')



def companyaccept(request,id):
  data=staff_details.objects.filter(id=id).update(Action=1)
  return redirect('staff_request')

def companyreject(request,id):
  data=staff_details.objects.get(id=id)
  
  data.delete()
  return redirect('staff_request')

def client_request(request):
  data = company_details.objects.filter(Action = 0).order_by('-id')
  all = company_details.objects.filter(Action = 1)
  return render(request,'admin/client_request.html',{'data': data,'all':all})

def client_details(request):
  data = company_details.objects.filter(Action = 1).order_by('-id')
  return render(request,'admin/client_details.html',{"data":data})

def staff_request(request):
  company =  company_details.objects.get(user = request.user)
  staff = staff_details.objects.filter(company=company,Action=0).order_by('-id')
  return render(request,'company/staff_request.html',{'staff':staff,'company':company})  
def View_staff(request):
  company =  company_details.objects.get(user = request.user)
  staff = staff_details.objects.filter(company=company,Action=0)
  allstaff = staff_details.objects.filter(company=company,Action=1).order_by('-id')

  return render(request, 'company/view_staff.html',{'staff':staff,'company':company,'allstaff':allstaff})



