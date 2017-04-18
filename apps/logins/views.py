from django.shortcuts import render, redirect
from .models import User, UserManager
from django.contrib import messages
import re
import bcrypt

def registrationPage(request):
	if "pageClear" not in request.session:
		request.session['pageClear']=True
		request.session['userID']=0
	else:
		request.session['fname_signedIn']=""
	if request.session['pageClear'] ==True:
		clear(request)
	context={"users": User.usermanager.all()}
	load_index_pg= render(request, "logins/registration.html", context)
	clear(request)
	request.session['userID']=0
	return load_index_pg

def register(request):
	request.session['validate'] = ""
	title = request.POST['title']
	firstName = request.POST['f_name']
	lastName = request.POST['l_name']
	maidenName = request.POST['m_name']
	birthday = request.POST['birthdate']
	email = request.POST['reg_email'].lower()
	password = request.POST['reg_pw']
	confPassword = request.POST['conf_reg_pw']
	user = User.usermanager.registerPerson(title, firstName, lastName, maidenName, birthday, email, password, confPassword, request)
	if user == True:
		return redirect('logins:success')
	else:
		return redirect('logins:index')
	

def login(request):
	entered_email = request.POST['login_email'].lower()
	entered_password = request.POST['login_password']
	user = User.usermanager.login(entered_email, entered_password, request)

	if user == False:
		return redirect('logins:index')
	else:
		request.session['userID']=user[1]
		request.session['pageClear']=True
		return redirect('logins:success')
		

def success(request):
	if request.session['userID']== 0:
		return redirect('logins:not_signed_in')
	else:
		signedInUser= User.usermanager.get(id=request.session['userID'])
		context = {"users":signedInUser}
		return render(request,"logins/success.html", context)

def delete(request, id):
	User.usermanager.filter(id=id).delete()
	return redirect('logins:index')

def clear(request):
	request.session['validate']=""
	request.session['title']=""
	request.session['fname']=""
	request.session['lname']=""
	request.session['mname']=""
	request.session['birthday']=""
	request.session['valEmail']=""
	request.session['loginEmail']=""
	request.session['pageClear']=False
	return redirect('logins:index')

def signout(request):
	request.session['userID']=0
	return redirect('main:index')

def not_signed_in(request):
	return render(request, "logins/not_signed_in.html")
	