from __future__ import unicode_literals

from django.db import models

class AddressManager(models.Manager):
	def createAddress(self, address, city,  state, zipcode, request):
		AddressFile.objects.create(address=address, city=city, state= state, zipcode= zipcode)
		usersAddress = AddressFile.objects.get(address=address, city=city, state= state, zipcode= zipcode)
		return usersAddress
	
	# def address_apt_relationship(self, sentAddress, sentAptNum, request):
	# 	sentAddress.aptNums.add(sentAptNum)
	# 	print "#"*50
	# 	sentAddress.save()

class AptNumManager(models.Manager):
	def createAptNum(self, theAptNum, request):
		AptNum.objects.create(apt_num=theAptNum)
		usersAptNum= AptNum.objects.get(apt_num=theAptNum)
		return usersAptNum

class AptNum(models.Model):
	apt_num=models.CharField(max_length=200)
	objects = AptNumManager()

	def __str__(self):
		return self.apt_num

class AddressFile(models.Model):
	address=models.CharField(max_length=500)
	city=models.CharField(max_length=100)
	state=models.CharField(max_length=100)
	zipcode=models.IntegerField()
	aptNums=models.ManyToManyField(AptNum, verbose_name="list of apartment numbers")
	objects = AddressManager()
