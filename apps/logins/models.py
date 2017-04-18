from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from ..addressApp.models import AddressFile, AptNum
import re
import bcrypt

class UserManager(models.Manager):
	def registerPerson(self, title, firstName, lastName, maidenName,birthday, email, password, confPassword,  request):

		emailRegXpass = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		nameRegXpass = re.compile(r'^[a-zA-Z]+\s?[a-zA-Z]+$')
		namespaceRegXpass = re.compile(r'^\s*[a-zA-Z]+\s?[a-zA-Z]+\s*$')
		first=firstName
		last=lastName
		valEm=email
		maidName=maidenName
		birth=birthday
		doesEMailExist=User.usermanager.filter(email=email)
		if len(firstName) < 2 or len(lastName) < 2:
			validate="-Enter First and Last Name (Must be 2 or more characters)"
		elif len(maidenName) != 0 and len(maidenName) < 2:
				validate="-Maiden Name is optional but if entered must be 2 or more characters"
		elif not nameRegXpass.match(maidenName) and len(maidenName) != 0:
			if namespaceRegXpass.match(maidenName):
				validate = "-Maiden Name is optional but should NOT Start or End with spaces. Please be sure you did not type an empty space at the beginning or ending of Maiden name"
			else:
				validate = "-Maiden Name is optional but can only contain letters, -- NO numbers, symbols, or special characters"
		elif not nameRegXpass.match(firstName):
			if namespaceRegXpass.match(firstName):
				validate = "-Names should NOT Start or End with spaces. Please be sure you did not type an empty space at the beginning or ending of your name"
			else:
				validate = "-Names can only contain letters, -- NO numbers, symbols, or special characters"
		elif not nameRegXpass.match(lastName):
			if namespaceRegXpass.match(lastName):
				validate = "-Names should NOT Start or End with spaces. Please be sure you did not type an empty space at the beginning or ending of your name"
			else:
				validate = "-Names can only contain letters, --NO numbers, symbols, or special characters"
		elif len(email) == 0:
			validate = "-Must Enter Email"
		elif not emailRegXpass.match(email):
			validate = "-Email invalid, please enter valid email"
		elif len(doesEMailExist) > 0:
			validate = "-Email already exists in database. Login Below or register with a different email."
		elif password != confPassword or len(password) < 8 or len(password) > 30:
			validate = "-Password and Confirm Password incorrect (Must match and be at least 8 characters - no more than 30)"
		else:
			request.session['pageClear']=True
			pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
			User.usermanager.create(title=title, firstName= firstName, lastName=lastName, maidenName=maidenName, birthday=birthday, email=email.lower(), password= pwhash)
			userDir=User.usermanager.filter(email=email)
			the_new_users_id=userDir[0].id
	# Address Add Area
	# Checking to see if address/aptNum already exists in database
			usersAddress=AddressFile.objects.filter(address=request.session['address'],zipcode=request.session['zipcode'])
			if request.session['aptNum'] !="":
				usersAptNum=AptNum.objects.filter(apt_num=request.session['aptNum'])
				if len(usersAptNum) < 1:
					aptNumber = request.session['aptNum']
					usersAptNum=AptNum.objects.createAptNum(aptNumber, request)
				else:
					usersAptNum = usersAptNum[0]

			else:
				usersAptNum=""

			print ">>>>>>>>>>>>>>>>>>>>>>>>>"
			print usersAptNum
			print"?%"*50
			

			if len(usersAddress)== 0:
				usersAddress = AddressFile.objects.createAddress(request.session['address'], request.session['city'], request.session['state'], request.session['zipcode'],request)
				print "^"*50
				print "usersAddress-not entered before"
				print usersAddress.address
			else:
				usersAddress=usersAddress[0]
				print "&"*50
				print "userAddress Found in database already"
				print usersAddress.address
			if usersAptNum != "":
				usersAddress.aptNums.add(usersAptNum)
				usersAddress.save()
				# AddressFile.objects.address_apt_relationship(usersAddress,usersAptNum, request)
			request.session['userID']=the_new_users_id
			return True
		request.session['validate'] = validate
		request.session['title']=title
		request.session['fname']=first
		request.session['lname']=last
		request.session['valEmail']=valEm
		request.session['mname']=maidName
		request.session['birthday']=birth
		return False

	def login(self, email, password, request):
		if len(User.usermanager.filter(email=email)) < 1:
			messages.error(request,"Email does not exist", extra_tags='loginError')
			return False
		else:
			user= User.usermanager.get(email=email)
			hashed = user.password.encode('utf-8')
			enteredPass = bcrypt.hashpw(password.encode('utf-8'), hashed)
			if hashed == enteredPass:
				request.session['loginEmail']=""
				return (True, user.id)

			else:
				request.session['loginEmail']= email
				messages.error(request, "-Email and/or password are not valid", extra_tags='loginError')
				return False

class User(models.Model):
	title=models.CharField(max_length=20)
	firstName=models.CharField(max_length=60)
	lastName=models.CharField(max_length=100)
	email=models.EmailField(max_length=150)
	password=models.CharField(max_length=200)
	maidenName=models.CharField(max_length=100, default="", blank=True)
	birthday=models.DateField()
	usermanager = UserManager()

		