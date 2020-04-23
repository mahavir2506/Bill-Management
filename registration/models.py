from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Store(models.Model):
	username=models.CharField(max_length=100)
	mobno=models.IntegerField()
	email=models.CharField(max_length=100)
	password=models.CharField(max_length=15)
	status=models.CharField(max_length=10)


	def __str__(self):
		return self.username

class Item(models.Model):
	item_id= models.AutoField(primary_key=True)
	name=models.CharField(max_length=10)
	price=models.IntegerField()
	sname=models.ForeignKey(Store,on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Bill(models.Model):
	bill_no=models.IntegerField()
	cust_name=models.CharField(max_length=100)
	sname=models.ForeignKey(Store,on_delete=models.CASCADE)
	bill=models.FileField(upload_to="bill/",blank=True)
