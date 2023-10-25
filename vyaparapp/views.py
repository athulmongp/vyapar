from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.utils.text import capfirst
from django.contrib import messages
from . models import *
import json
from django.http.response import JsonResponse
from django.utils.crypto import get_random_string
from datetime import date
from datetime import timedelta

# Create your views here.
def home(request):
  return render(request, 'home.html')



    
def homepage(request):
  com =  company.objects.get(user = request.user)
  allmodules= modules_list.objects.get(company=com.id,status='New')
  context = {
              'company' : com,
              'allmodules':allmodules
          }
  return render(request, 'company/homepage.html', context)

def staffhome(request,id):
  staff =  staff_details.objects.get(id=id)
  allmodules= modules_list.objects.get(company=staff.company,status='New')
  context = {
              'staff' : staff,
              'allmodules':allmodules

          }
  return render(request, 'staff/staffhome.html', context)
def adminhome(request):
 
  
  
  return render(request, 'admin/adminhome.html')




# @login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

def view_profile(request):
  com =  company.objects.get(user = request.user) 
  selected_options = request.session.get('selected_options', None)
  
  context = {
              'company' : com,
              'selected_options': json.dumps(selected_options)
          }
  return render(request,'profile.html',context)
  
def edit_profile(request,pk):
  com= company.objects.get(id = pk)
  user1 = User.objects.get(id = com.user_id)
  selected_options = request.session.get('selected_options', None)

  if request.method == "POST":

      user1.first_name = capfirst(request.POST.get('f_name'))
      user1.last_name  = capfirst(request.POST.get('l_name'))
      user1.email = request.POST.get('email')
      com.contact_number = request.POST.get('cnum')
      com.address = capfirst(request.POST.get('ards'))
      com.company_name = request.POST.get('comp_name')
      com.company_email = request.POST.get('comp_email')
      com.city = request.POST.get('city')
      com.state = request.POST.get('state')
      com.country = request.POST.get('country')
      com.pincode = request.POST.get('pinc')
      com.gst_num = request.POST.get('gst')
      com.pan_num = request.POST.get('pan')
      com.business_name = request.POST.get('bname')
      com.company_type = request.POST.get('comp_type')
      if len(request.FILES)!=0 :
          com.profile_pic = request.FILES.get('file')

      com.save()
      user1.save()
      return redirect('view_profile')

  context = {
      'company' : com,
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
  com =  company.objects.get(user = request.user)
  selected_options = request.session.get('selected_options', None)
  
  context = {
              'company' : com,
              'selected_options': json.dumps(selected_options),
              
          }
  return render(request, 'company/settings.html',context)

def hide_options(request):
    
    com =  company.objects.get(user = request.user)
    if request.method == 'POST':
        selected_options = list(request.POST.getlist('selected_options'))

    request.session['selected_options'] = selected_options
    
    context = {'selected_options': json.dumps(selected_options),
               'company' : com}
   
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
        cust_data = company( contact=mobile,
                             user = data)
        cust_data.save()
        
        return redirect('company_reg2')
      else:
        messages.info(request, 'Sorry, Email already exists')
        return redirect('company_reg')
    return render(request,'company/register.html')  
def company_reg2(request):
  terms=payment_terms.objects.all()
  
  return render(request,'company/register2.html',{'terms':terms})  
def add_company(request):
  
  print(id)
  if request.method == 'POST':
    email=request.POST['email']
    user=User.objects.get(email=email)
    
    c =company.objects.get(user = user)
    c.company_name=request.POST['cname']

    c.address=request.POST['address']
    c.city=request.POST['city']
    c.state=request.POST['state']
    c.country=request.POST['country']
    c.pincode=request.POST['pincode']
    c.pan_number=request.POST['pannumber']
    c.gst_type=request.POST['gsttype']
    c.gst_no=request.POST['gstno']
    c.profile_pic=request.FILES.get('image')

    select=request.POST['select']
    terms=payment_terms.objects.get(id=select)
    c.dateperiod=terms
    c.start_date=date.today()
    days=int(terms.days)

    
    end= date.today() + timedelta(days=days)
    c.End_date=end


    
    

    code=get_random_string(length=6)
    if company.objects.filter(Company_code = code).exists():
       code2=get_random_string(length=6)
       c.Company_code=code2
    else:
      c.Company_code=code

   
    c.save()
    # messages.success(request, 'Welcome'+ ' ' +  user.first_name +' '+user.last_name + ' ')

    return redirect('Allmodule',user.id)  
  return render(request,'company/register2.html')   

def staff_register(request):
  com=company.objects.all()

  return render(request, 'staff/staffreg.html',{'company':com})

def staff_registraction(request):
  if request.method == 'POST':
    fn=request.POST['fname']
    ln=request.POST['lname']
    email=request.POST['eid']
    un=request.POST['uname']
    pas=request.POST['pass']
    ph=request.POST['ph']
    code=request.POST['code']
    com=company.objects.get(Company_code=code)
    img=request.FILES.get('image')

    if staff_details.objects.filter(user_name=un).exists():
      messages.info(request, 'Sorry, Username already exists')
      print("1")
      return redirect('staff_register')
    elif staff_details.objects.filter(email=email).exists():
      messages.info(request, 'Sorry, Email already exists')
      print("2")
      return redirect('staff_register')
    else:
      
      staff=staff_details(first_name=fn,last_name=ln,email=email,user_name=un,password=pas,contact=ph,img=img,company=com)
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
        data=company.objects.get(user=request.user)
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
  data=company.objects.filter(id=id).update(Action=1)
  return redirect('client_request')
def adminreject(request,id):
  data=company.objects.get(id=id)
  data.user.delete()
  data.delete()
  return redirect('client_request')



def companyaccept(request,id):
  data=staff_details.objects.filter(id=id).update(Action=1)
  return redirect('staff_request')

def companyreject(request,id):
  data=staff_details.objects.get(id=id)
  
  data.delete()
  return redirect('staff_request')

def client_request(request):
  data = company.objects.filter(Action = 0).order_by('-id')
  all = company.objects.filter(Action = 1)
  return render(request,'admin/client_request.html',{'data': data,'all':all})

def client_request_overview(request,id): 
  com = company.objects.get(id=id)
  allmodules=modules_list.objects.get(company=id)
  return render(request,'admin/client_request_overview.html',{'company':com,'allmodules':allmodules})

def client_details(request):
  data = company.objects.filter(Action = 1).order_by('-id')
  return render(request,'admin/client_details.html',{"data":data})
def client_details_overview(request,id): 
  com = company.objects.get(id=id)
  allmodules=modules_list.objects.get(company=id)
  return render(request,'admin/client_details_overview.html',{'company':com,'allmodules':allmodules})

def staff_request(request):
  com =  company.objects.get(user = request.user)
  staff = staff_details.objects.filter(company=com,Action=0).order_by('-id')
  allmodules= modules_list.objects.get(company=com.id,status='New')
  return render(request,'company/staff_request.html',{'staff':staff,'company':com,'allmodules':allmodules}) 
 
def View_staff(request):
  com =  company.objects.get(user = request.user)
  staff = staff_details.objects.filter(company=com,Action=0)
  allstaff = staff_details.objects.filter(company=com,Action=1).order_by('-id')
  allmodules= modules_list.objects.get(company=com.id,status='New')

  return render(request, 'company/view_staff.html',{'staff':staff,'company':com,'allstaff':allstaff,'allmodules':allmodules})

def payment_term(request):
  terms = payment_terms.objects.all()
  
  return render(request,'admin/payment_terms.html',{'terms':terms})
def add_payment_terms(request):
  if request.method == 'POST':
    num=int(request.POST['num'])
    select=request.POST['select']
    if select == 'Years':
      days=int(num)*365
      pt = payment_terms(payment_terms_number = num,payment_terms_value = select,days = days)
      pt.save()
      messages.info(request, 'Payment term is added')
      return redirect('payment_term')

    else:  
      days=int(num*30)
      pt = payment_terms(payment_terms_number = num,payment_terms_value = select,days = days)
      pt.save()
      messages.info(request, 'Payment term is added')
      return redirect('payment_term')


  return redirect('payment_term')

def Allmodule(request,uid):
  user=User.objects.get(id=uid)
  return render(request,'company/modules.html',{'user':user})

def addmodules(request,uid):
  if request.method == 'POST':
    com=company.objects.get(user=uid)
    c1=request.POST.get('c1')
    c2=request.POST.get('c2')
    c3=request.POST.get('c3')
    c4=request.POST.get('c4')
    c5=request.POST.get('c5')
    c6=request.POST.get('c6')
    c7=request.POST.get('c7')
    c8=request.POST.get('c8')
    c9=request.POST.get('c9')
    c10=request.POST.get('c10')
    c11=request.POST.get('c11')
    c12=request.POST.get('c12')
    c13=request.POST.get('c13')
    c14=request.POST.get('c14')
    
    data=modules_list(company=com,sales_invoice = c1,
                      Estimate=c2,Payment_in=c3,sales_order=c4,
                      Delivery_challan=c5,sales_return=c6,Purchase_bills=c7,
                      Payment_out=c8,Purchase_order=c9,Purchase_return=c10,
                      Bank_account=c11,Cash_in_hand=c12, cheques=c13,Loan_account=c14)
    data.save()

    return redirect('log_page')
  


def companyreport(request):
  com =  company.objects.get(user = request.user)
  allmodules= modules_list.objects.get(company=com.id,status='New')
  return render(request,'company/companyreport.html',{'company':com,'allmodules':allmodules})  

def Companyprofile(request):
  com =  company.objects.get(user = request.user)
  allmodules= modules_list.objects.get(company=com.id,status='New')
  return render(request,'company/companyprofile.html',{'company':com,'allmodules':allmodules})

def editcompanyprofile(request):
  com =  company.objects.get(user = request.user)
  allmodules= modules_list.objects.get(company=com.id,status='New')
  terms=payment_terms.objects.all()
  return render(request,'company/editcompanyprofile.html',{'company':com,'allmodules':allmodules,'terms':terms})

def editcompanyprofile_action(request):
  com =  company.objects.get(user = request.user)
  if request.method == 'POST':
    com.company_name = request.POST['cname']
    com.user.email = request.POST['email']
    com.contact = request.POST['ph']
    com.address = request.POST['address']
    com.city = request.POST['city']
    com.state = request.POST['state']
    com.country = request.POST['country']
    com.pincode = request.POST['pincode']

    t = request.POST['select']
    terms = payment_terms.objects.get(id=t)
    com.dateperiod = terms
    com.start_date=date.today()
    days=int(terms.days)

    end= date.today() + timedelta(days=days)
    com.End_date=end

    old=com.profile_pic
    new=request.FILES.get('image')
    if old!=None and new==None:
      com.profile_pic=old
    else:
      com.profile_pic=new
    
    com.save() 
    com.user.save() 
    return redirect('Companyprofile') 



  return redirect('Companyprofile')

def editmodule(request):
  com =  company.objects.get(user = request.user)
  allmodules= modules_list.objects.get(company=com.id,status='New')
  return render(request,'company/editmodule.html',{'company':com,'allmodules':allmodules})

def editmodule_action(request):
  if request.method == 'POST':
    com = company.objects.get(user = request.user)
    if modules_list.objects.filter(company=com.id,status='Old').exists():
      old=modules_list.objects.filter(company=com.id,status='Old')
      old.delete()

    old_data=modules_list.objects.get(company=com.id,status='New')  
    old_data.status='Old'
    old_data.save()



    c1=request.POST.get('c1')
    c2=request.POST.get('c2')
    c3=request.POST.get('c3')
    c4=request.POST.get('c4')
    c5=request.POST.get('c5')
    c6=request.POST.get('c6')
    c7=request.POST.get('c7')
    c8=request.POST.get('c8')
    c9=request.POST.get('c9')
    c10=request.POST.get('c10')
    c11=request.POST.get('c11')
    c12=request.POST.get('c12')
    c13=request.POST.get('c13')
    c14=request.POST.get('c14')
    
    data=modules_list(company=com,sales_invoice = c1,
                      Estimate=c2,Payment_in=c3,sales_order=c4,
                      Delivery_challan=c5,sales_return=c6,Purchase_bills=c7,
                      Payment_out=c8,Purchase_order=c9,Purchase_return=c10,
                      Bank_account=c11,Cash_in_hand=c12, cheques=c13,Loan_account=c14)
    data.save()
    data1=modules_list.objects.filter(company=com.id,status='New').update(update_action=1)
    return redirect('Companyprofile')
    
    
  return redirect('Companyprofile')

def admin_notification(request):
  data= modules_list.objects.filter(update_action=1,status='New')

  return render(request,'admin/admin_notification.html',{'data':data})

def module_updation_details(request,mid):
  data= modules_list.objects.get(id=mid)
  allmodules= modules_list.objects.get(company=data.company,status='New')
  old_modules = modules_list.objects.get(company=data.company,status='Old')

  return render(request,'admin/module_updation_details.html',{'data':data,'allmodules':allmodules,'old_modules':old_modules})

def module_updation_ok(request,mid):
  data1=modules_list.objects.filter(id=mid).update(update_action=0)
  return redirect('admin_notification')

def staff_profile(request,sid):
  staff =  staff_details.objects.get(id=sid)
  allmodules= modules_list.objects.get(company=staff.company,status='New')
  context = {
              'staff' : staff,
              'allmodules':allmodules

          }
  return render(request,'staff/staff_profile.html',context)

def editstaff_profile(request,sid):
  staff =  staff_details.objects.get(id=sid)
  allmodules= modules_list.objects.get(company=staff.company,status='New')
  context = {
              'staff' : staff,
              'allmodules':allmodules

          }
  return render(request,'staff/editstaff_profile.html',context)

def editstaff_profile_action(request,sid):
  if request.method == 'POST':
    staff =  staff_details.objects.get(id=sid)
    staff.first_name = request.POST['fname']
    staff.last_name = request.POST['lname']
    staff.user_name = request.POST['uname']
    staff.email = request.POST['email']
    staff.contact = request.POST['ph']
    old=staff.img
    new=request.FILES.get('image')
    if old!=None and new==None:
      staff.img=old
    else:
      staff.img=new

    staff.save()  

    return redirect ('staff_profile',staff.id)
  return redirect ('staff_profile',staff.id)









