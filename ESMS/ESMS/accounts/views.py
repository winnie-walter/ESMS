
from django.http.response import HttpResponse
from django.shortcuts import redirect, render,HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,auth,Group,Permission
from django.contrib import messages
from .models import *
from django.contrib.auth.hashers import make_password,check_password
import datetime
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import ExtractYear
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import EmailMessage
# Create your views here.
def home(request):
    
    
    return render(request,'home.html')

def dashboard(request):
    
    user = User.objects.all()
    return render(request,'dashboard.html',{'u':user})                                                                                         

def login(request):
       
    if request.method=='POST':

     username = request.POST.get("username")
     password = request.POST.get("password")

     user = auth.authenticate(username=username,password=password)

     if user is not None:

           
            auth.login(request,user)
            return redirect('/dashboard')
     else:
         return redirect('/login')

    return render(request,'signup_login.html')

def register(request):
    
  
    u = User()
    g=Admins()

    if request.method == 'POST':
        fname = request.POST.get("fname")
        mname = request.POST.get("mname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        phone=request.POST.get("phone")
        if User.objects.filter(username=username).exists():
            messages.info(request,'user already exists')
            return redirect('/register')    

        if (password1 == password2):
         u.username=username
         u.first_name=fname
         u.last_name=lname
          
         u.password=make_password(password1)
         u.save()
         
   	 # if ser is a one to one relation to that table eg guest
         g.user=u
         g.phone_number=phone
         g.middle_name=mname
         g.save()
         messages.info(request,'successful')
         return render(request,'signup_login.html')
        

        else:
         messages.error(request,'mismatch password')

    

    return render(request,'signup_login.html')
                                                                                         
def dashboard(request):
    
    
    return render(request,'dashboard.html')

def manageuser(request):
    
    a = Admins.objects.exclude(user__username=request.user.username).filter(is_deleted='False').order_by('id')
    context = {'a': a}
    return render(request,'manageuser.html',context)

def adduser(request):
    u = User()
    g=Admins()
    r = Group.objects.all()
    # p =Admins.objects.get()
    
    # k = Group.objects.get(name="Admin")
    dt = datetime.date.today()
    if request.method == 'POST':
        fname = request.POST.get("fname")
        mname = request.POST.get("mname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        password1 = '12345'
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        phone=request.POST.get("phone")
        gender = request.POST.get("gender")
        if(str(dt)<dob):
            messages.error(request,"insert date before today")
            return redirect("/adduser")
        # for i in Group.objects.all():
        #      p.user.groups.remove(i.id)

        r_id=[]
        permission = [x.name for x in Group.objects.all()]

        for i in permission:
             
             r_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
        if User.objects.filter(username=username).exists():
            messages.info(request,'user already exists')
            return redirect('/adduser')

        u.username=username
        u.first_name=fname
        u.last_name=lname
        
        u.password=make_password(password1)
        u.save()
        # u.groups.add(k)
        g.user=u
        g.phone_number=phone
        g.middle_name=mname
        g.dob=dob
        g.address=address
        g.gender=gender
        g.save()
        for r in r_id:
               u.groups.add(Group.objects.get(id=r))
        message = "Here is your Login credentials \n Email: "+username+"\n"+"Password: "+password1+"\n \n"+"Welcome"
        send_mail('Welcome To Event Sharing Management System',message,'systemdevelopment8@gmail.com',[username],
          fail_silently=False)
        messages.info(request,'successful user was added')
        return redirect('/adduser')
        
    return render(request,'adduser.html',{'r':r})
def eventtype(request):
  e = EventType.objects.all()


  return render(request,'manageeventtype.html',{'e':e})

def addevent_type(request):
    if request.method=='POST':
        eventtype = request.POST.get('Event_type')
        EventType.objects.create(name = eventtype)
        return redirect('/eventtype')


    return render(request,'addevent_type.html') 


def editevent_type(request,pk):
    e = EventType.objects.filter(id=pk)

    if request.method=='POST':
        eventtype = request.POST.get('Event_type')
        EventType.objects.filter(id=pk).update(name = eventtype)
        return redirect('/eventtype')



    return render(request,'editevent_type.html',{'e':e})

def deleteevent_type(request,pk):
    EventType.objects.filter(id=pk).delete()


    return redirect('/eventtype')

def deleteevent(request,pk):
    Event.objects.filter(id=pk).delete()


    return redirect('/manageevent')   

def editevent(request,pk):
    e = Event.objects.filter(id=pk)
    s= EventType.objects.all()
    a= Admins.objects.all()
    
    if request.method=='POST':
      eventname=request.POST['eventname']
      location=request.POST['location']
      time=request.POST['time']
      type_id =request.POST['type']
      types = EventType.objects.get(id=type_id)
      user_id=request.POST['user']
      
      user=Admins.objects.get(id=user_id)
      image = request.FILES.get('file')
      Event.objects.filter(id=pk).update(name=eventname,location=location,time=time,eventtype=types,user=user,card=image)
      return redirect('/manageevent')

    return render(request,'editevent.html',{'e':e,'s':s,'a':a}) 

        
def edituser(request,pk):
    u = Group.objects.all()
    a = Admins.objects.filter(user__id=pk)
    p =Admins.objects.get(user__id=pk)
    exclude_perm = [1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,29,30,31,32,33,34,35,36]
    x = Permission.objects.exclude(id__in=exclude_perm)
    if request.method == 'POST':
        fname = request.POST.get("fname")
        mname = request.POST.get("mname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        address = request.POST.get("address")
        dob = request.POST.get("dob")
        phone=request.POST.get("phone")
        gender = request.POST.get("gender")  
        User.objects.filter(id=pk).update(first_name=fname,last_name=lname,username=username)
        Admins.objects.filter(user_id=pk).update(middle_name=mname,address=address,dob=dob,phone_number=phone,gender=gender)
        
        for j in Permission.objects.all():
              p.user.user_permissions.remove(j.id)
        for i in Group.objects.all():
             p.user.groups.remove(i.id)
        
        r_id=[]
        s_id=[]
        permission = [x.name for x in Group.objects.all()]
        perm = [i.name for i in Permission.objects.all()] 
        
        for i in permission:
             
             s_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
             
                
        for i in perm:
             
             r_id.append(int(request.POST.get(i))) if request.POST.get(i) else print("")
        
        try:
        
            profile = request.FILES.get("profile")
            file_name = request.FILES['profile'].name
            fs = FileSystemStorage()
            files = fs.save(profile.name,profile)
            fileurl = fs.url(files)
            report = file_name    
                    
            Admins.objects.filter(user_id=pk).update(profile=profile)
        
        except MultiValueDictKeyError:
                file_name = False
        for r in r_id:
               p.user.user_permissions.add(Permission.objects.get(id=r))
               
        for r in s_id:
               p.user.groups.add(Group.objects.get(id=r))
        messages.success(request,'update successful')    
        return HttpResponseRedirect(request.path_info)
    return render(request,'edituser.html',{'a':a,'x':x,'u':u})

def deleteuser(request,pk):
    
    User.objects.filter(id=pk).delete()
    
    return redirect('/trash')

def removeuser(request,pk):
      u = User.objects.filter(id=pk).filter(is_active='True')
      my_date = datetime.datetime.now()
     

      if u:
           User.objects.filter(id=pk).update(is_active='False')
           Admins.objects.filter(user__id=pk).update(is_deleted='True',deleted_at=my_date)    
           return redirect('/manageuser')
      return redirect('/manageuser')
       

def manageevent(request):
    n= Event.objects.all()
    
    
    return render(request,'manageevent.html',{'n':n})

def addevent(request):
    s= EventType.objects.all()
    a = Admins.objects.all()
    if request.method=="POST":
      eventname=request.POST['eventname']
      location=request.POST['location']
      time=request.POST['time']
      type_id =request.POST['type']
      types = EventType.objects.get(id=type_id)
      user_id=request.POST['user']
      
      user=Admins.objects.get(id=user_id)
      image = request.FILES.get('file')
      Event.objects.create(name=eventname,location=location,time=time,eventtype=types,user=user,card=image)
      return redirect('/manageevent')
    return render(request,'addevent.html',{'s':s,'a':a})


def changepassword(request):
    if request.method =='POST':
      old = request.POST.get("old")
      new = request.POST.get("password1")
      comf = request.POST.get("password2")
      if ((request.user.check_password(old)) and (new == comf)):
              
       user = User.objects.filter(username=request.user.username).update(password=make_password(new))      
 
       messages.success(request,'successful password changed login again')
       return redirect('/login')
      else:
           messages.success(request,'mismatch password')
           return redirect('/changepassword')
    return render(request,'changepassword.html')

def profile(request):

    event = Event.objects.all().count
    today = datetime.date.today()
  
    d = Admins.objects.get(dob=request.user.admins.dob)

    o = d.dob
    age = int((today - o).days/363.25)
    et= Event.objects.all().distinct('eventtype').count
    g= Guest.objects.all().distinct('event').count
    context={'event':event,'et':et,'g':g,'d':d,'o':o,'age':age}
    u = User()
    if request.method =='POST':
         
      fname = request.POST.get("fname")
      lname = request.POST.get("lname")
      username = request.POST.get("username")
      mname = request.POST.get("mname")
      dob = request.POST.get("dob")
      address = request.POST.get("address")
      phone = request.POST.get("phone")
      gender = request.POST.get("gender")
     
    
      user = User.objects.filter(username=request.user.username).update(first_name=fname,last_name=lname,username=username)
      admin = Admins.objects.filter(id = request.user.admins.id).update(middle_name=mname,address=address,phone_number=phone,gender=gender,dob=dob)
    #   
    
      try:
        
        profile = request.FILES.get("profile")
        file_name = request.FILES['profile'].name
        fs = FileSystemStorage()
        files = fs.save(profile.name,profile)
        fileurl = fs.url(files)
        report = file_name    
                
        admin = Admins.objects.filter(id = request.user.admins.id).update(profile=profile)
    
      except MultiValueDictKeyError:
            file_name = False
      messages.success(request,'update successful')      
      return redirect('/profile')
    return render(request,'profile.html',context)

def blockuser(request,pk):
      u = User.objects.filter(id=pk).filter(is_active='True')
     
      if u:      
       User.objects.filter(id=pk).update(is_active='False')   
      else:
         User.objects.filter(id=pk).update(is_active='True') 
      return redirect('/manageuser') 
    

def logout(request):


    auth.logout(request)

    return redirect('/')

def managerole(request):
       
      g = Group.objects.all()
      r = Permission.objects.all()
      return render(request,'managerole.html',{'r':r,'g':g})

def sendevent(request):
   
    w = Event.objects.all()
    a = Guest()
    if request.method=='POST':
        x=request.POST['Gname']
        p=request.POST['email']
        r=request.POST['eventtype']
        j=Event.objects.get(id=r)
        l = Event.objects.filter(id=r)
        Guest.objects.create(fullname=x,email=p,event=j)
        msg = EmailMessage('welcome',x, 'systemdevelopment8@gmail.com', [p])
        msg.conen_subpe = "html"
        msg.attach_file(r+'.png')
        msg.send()
        return redirect('/sendevent')

    return render(request,'sendevent.html',{'w':w} )


def addrole(request):
   p = Group()
   g = Group.objects.all()
   exclude_perm = [1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,33,34,35,36]
   r = Permission.objects.exclude(id__in=exclude_perm)
   if request.method == "POST":
      name = request.POST.get("name")
      permission = [x.name for x in Permission.objects.all()]
      s_id = []
      p.name=name
      for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      p.save()
      for s in s_id:
           p.permissions.add(Permission.objects.get(id=s))   
      return redirect('/managerole')  
   return render(request,'addrole.html',{'r':r})

def editrole(request,pk):

   exclude_perm = [1,2,3,4,13,14,15,16,17,18,19,20,21,22,23,24,29,30,31,32,33,34,35,36]
   p = Permission.objects.exclude(id__in=exclude_perm)
   r = Group.objects.filter(id=pk)
   y=Group.objects.get(id=pk)
   if request.method == 'POST':
    name = request.POST.get('name')
    
             
    for j in Permission.objects.all():
              y.permissions.remove(j.id) 
      
      
    permission = [x.name for x in Permission.objects.all()]
     
    s_id = []
    Group.objects.filter(id=pk).update(name=name)
    for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
    r=Group.objects.filter(id=pk).update(name=name)
      
    for s in s_id:
           y.permissions.add(Permission.objects.get(id=s))  
    return redirect('/managerole')
           
   return render(request,'editrole.html',{'r':r,'p':p})

def grantRole(request,pk):
    g=Group.objects.all()
             
    # d=Admins.objects.all()
    u = User.objects.get(id=pk)
    d=Admins.objects.filter(user__id=pk)
    p = Admins.objects.get(user__id=pk)
    r = Group.objects.filter(id=pk)
    
    if request.method == 'POST':
        
      for i in Group.objects.all():
             u.groups.remove(i.id)
             
      permission = [x.name for x in Group.objects.all()]
      s_id = []
      
      for x in permission:
             s_id.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
      
      for s in s_id:
           u.groups.add(Group.objects.get(id=s))  
      return redirect('/manageuser')
    return render(request, 'grantRole.html',{'g':g,'d':d,'u':u})

def deleterole(request,pk):
    
    Group.objects.filter(id=pk).delete()
    
    return redirect('/managerole')

def trash(request):
    
    g=Admins.objects.filter(is_deleted='True')                  
    
    
    return render(request, 'trash.html',{'g':g})           
               
def restore(request,pk):   

  User.objects.filter(id=pk).update(is_active='True')
  Admins.objects.filter(user__id=pk).update(is_deleted='False')                  
      
    
  return redirect('/trash')
