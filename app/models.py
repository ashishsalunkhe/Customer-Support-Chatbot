# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from datetime import date
#Create your models here.

class ChatDetals(models.Model):
    User = models.CharField(max_length=100)
    Bot = models.TextField(null=True, blank=True)
    Chat_Time = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return u"%s" % self.name

class CateGory(models.Model):
    FruitNo = models.IntegerField(blank=True, null=True)
    category = models.TextField(null=True, blank=True)
    tag = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return u"%s" % self.name

class CartList(models.Model):
    FruitNo = models.IntegerField(blank=True, null=True)
    CartItem = models.TextField(null=True, blank=True)
    def __unicode__(self):
        return u"%s" % self.name

class Orders(models.Model):
    FruitNo = models.IntegerField(blank=True, null=True)
    CartItem = models.TextField(null=True, blank=True)

class Product(models.Model):
    # fruitCategory = models.ForeignKey(Category, on_delete=models.CASCADE)
    FruitNo = models.IntegerField(blank=True, null=True)
    fruitName = models.CharField(max_length=100)
    fruitPrice = models.IntegerField()
    Unit = models.TextField(blank=True, null=True)
    FruitsSize = models.TextField(blank=True, null=True)
    fruitQuantity = models.IntegerField()
    fruitDiscount = models.IntegerField()
    fruitBill = models.IntegerField()

class AI_ChatBotDetails(models.Model):
    FruitsID = models.TextField(blank=True, null=True)
    FruitNo = models.IntegerField(blank=True, null=True)
    ImageID = models.IntegerField(blank=True, null=True)
    FruitsTag = models.TextField(blank=True, null=True)
    FruitsName = models.TextField(blank=True, null=True)
    FruitsSize = models.TextField(blank=True, null=True)
    FruitPrice = models.IntegerField()
    Unit = models.TextField(blank=True, null=True)
    FruitDiscount = models.IntegerField()
    FruitBill = models.IntegerField()

    def __unicode__(self):
        return u"%s" % self.name

class fruits_List(models.Model):
    FruitsID = models.IntegerField(blank=True, null=True)
    FruitNo = models.IntegerField(blank=True, null=True)
    ImageID = models.IntegerField(blank=True, null=True)
    FruitsTag = models.TextField(blank=True, null=True)
    FruitsName = models.TextField(blank=True, null=True)
    FruitsSize = models.TextField(blank=True, null=True)
    FruitPrice = models.IntegerField()
    Unit = models.TextField(blank=True, null=True)
    FruitDiscount = models.IntegerField()
    FruitBill = models.IntegerField()

    def __unicode__(self):
        return u"%s" % self.name

    def __unicode__(self):
        return u"%s" % self.name
