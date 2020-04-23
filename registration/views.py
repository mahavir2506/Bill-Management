from django.shortcuts import render
from django.contrib.auth.models import User
from registration.models import Store,Item
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from registration.utills import render_to_pdf
from registration.models import Bill
from io import BytesIO
from django.core.files import File
billlist=[]
c_user=""
cust_name=""
total=0
# Create your views here.
def index(request):
	if request.method=="POST":
		if request.POST["password"]==request.POST["password1"]:
			try:
				user=User.objects.get(username=request.POST["username"])
				print(user)
				return render(request,"registration/signup.html",{"error":"user already exit"})
			except:
				a=Store()
				a.username=request.POST["username"]
				a.email=request.POST["email"]
				a.mobno=request.POST["mobno"]
				a.password=request.POST["password"]
				a.status="denied"
				a.save()
				user=User.objects.create_user(username=request.POST["username"],password=request.POST["password"])
				mail_subject = 'Activate your account.'
				message = render_to_string('registration/acc_active_email.html',{'user': request.POST["username"],'domain': "http://127.0.0.1:8000/active/"+request.POST["username"],})
				to_email = request.POST["email"]
				email =EmailMessage(mail_subject, message, to=[to_email])
				email.send()
				return HttpResponse('Please confirm your email address to complete the registration')
				#auth.login(request,user)
				#return render(request,"registration/signup.html")
		else:
			return render(request,"registration/signup.html",{"error":"password and repeate password must be match"})
	else:
		global c_user
		if c_user:
			return redirect("home")
		else:
			return render(request,"registration/signup.html")
		return render(request,"registration/signup.html")
			


def login(request):
	if request.method=="POST":
		user=auth.authenticate(username=request.POST["username"],password=request.POST["password"])
		
		if user:
			a=Store.objects.get(username=request.POST["username"])
			if a.status=="active":
				global c_user
				c_user=request.POST["username"]
				auth.login(request,user)
				return redirect("home")

			else:
				return HttpResponse('Please confirm your email address to complete the registration')
		else:
			return render(request,"registration/login.html",{"error":"username or password wrong"})
	else:
		return render(request,"registration/login.html")

@login_required()
def logout(request):
	global billlist
	global c_user
	billlist.clear()
	c_user=""	
	auth.logout(request)
	return render(request,"registration/login.html")

def active(request,username):
	a=Store.objects.get(username=username)
	a.status="active"
	a.save()
	return render(request,"registration/login.html")

def forget(request):
	if request.method=="POST":
		a=Store.objects.get(username=request.POST["username"])
		mail_subject = 'account password.'
		message = render_to_string('registration/acc_active_email.html',{'user':"your password is : \n"+a.password,'domain': "http://127.0.0.1:8000/login",})
		to_email = a.email
		email =EmailMessage(mail_subject, message, to=[to_email])
		email.send()
		return HttpResponse("<h1> password reactivate succes </h1>")
	else:
		return render(request,"registration/forget.html")	
@login_required()
def home(request):
	global c_user
	global billlist
	global cust_name
	global total
	if request.method=="POST":
		a=Store.objects.get(username=c_user)
		d={}
		cust_name=request.POST["cname"]
		d["item"]=request.POST["itemselect"]
		d["qty"]=request.POST["qty"]
		#print(d["qty"])
		k=Item.objects.get(name=request.POST["itemselect"])
		d["price"]=k.price
		d["total"]=int(d["qty"]) * int(d["price"])
		total=total+d["total"]
		billlist.append(d)
		b=Item.objects.all()
		item=[]
		for i in b:
			#print("username:"+i.sname.username)
			if i.sname.username == a.username:
				item.append(i.name)
		return render(request,"registration/home.html",{"item":item,"username":a.username,"mobno":a.mobno,"billlist":billlist})
	else:
		b=Item.objects.all()
		item=[]
		for i in b:
			if i.sname.username==c_user:
				item.append(i.name)
		return render(request,"registration/home.html",{"item":item,"username":c_user,"mobno":Store.objects.get(username=c_user).mobno})
@login_required()
def print(request):
	if request.method=="GET":
		global billlist
		global c_user
		global cust_name
		global total
		billno=0
		a=Bill()
		b=Bill.objects.all()
		for i in b:
			if i.sname.username==c_user:
				if i.bill_no:
					billno=i.bill_no		
				else:
					billno=0
		billno=billno+1
		data = {'user':cust_name,'billlist': billlist,"total":total}
		pdf = render_to_pdf('registration/invoice.html',data)
		filename=c_user+"_"+str(billno)
		a.bill_no=billno
		a.cust_name=cust_name
		a.sname=Store.objects.get(username=c_user)
		a.save()
		d=Bill.objects.get(bill_no=billno,sname=Store.objects.get(username=c_user))
		d.bill.save(filename, File(BytesIO(pdf.content)))
		return HttpResponse(pdf, content_type='application/pdf')
@login_required()
def additem(request):
	global c_user
	if request.method=="POST":
		a=Item()
		a.name=request.POST["name"]
		a.price=request.POST["price"]
		a.sname=Store.objects.get(username=c_user)
		a.save()
		return redirect("home")
	else:
		return render(request,"registration/additem.html")	

@login_required()
def itemlist(request):
	global c_user
	b=Item.objects.all()
	item=[]
	for i in b:
		if i.sname.username == c_user:
			d={}
			d["name"]=i.name
			d["id"]=i.item_id
			item.append(d)
	return render(request,"registration/itemlist.html",{"item":item})

@login_required()
def itemcrud(request,pk):
	#print(pk)
	a=Item.objects.get(item_id=pk)
	return render(request,"registration/itemcrud.html",{"item":a})

@login_required()
def itemupdate(request,pk):
	a=Item.objects.get(item_id=pk)
	a.name=request.POST["name"]
	a.price=request.POST["price"]
	a.save()
	return redirect("home")


@login_required()
def itemdelete(request,pk):
	a=Item.objects.get(item_id=pk)
	a.delete()
	return redirect("home")
