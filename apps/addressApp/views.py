from django.shortcuts import render, redirect
from .models import AddressFile, AptNum, AddressManager, AptNumManager

def index(request):
	if "address" not in request.session:
		request.session['address']=""
		request.session['aptNum']=""
		request.session['city']=""
		request.session['state']=""
		request.session['zipcode']=""	
	context={ "addressInfo" : AddressFile.objects.all()}
	return render(request, 'addressApp/addressEnterVerify.html', context)

def sessions_address(request):
	request.session['address']= request.POST['address']
	request.session['aptNum']=request.POST['aptNum']
	request.session['city']= request.POST['city']
	request.session['state']= request.POST['state']
	request.session['zipcode']= request.POST['zipcode']

	return redirect('logins:index')


def delete(request, id):
	AddressFile.objects.filter(id=id).delete()
	return redirect('address:index')