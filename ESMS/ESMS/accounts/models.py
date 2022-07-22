from django.db import models
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.files import File# Create your models here.
import random

from django.contrib.auth.models import User

class Admins(models.Model):
    
    GENDER = (('Male', 'MALE'), 
    ('Female','FEMALE'),('Others', 'Others')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100,null=True, blank=True)
    phone_number = models.CharField(max_length=100,null=True, blank=True)
    address= models.CharField(max_length=200,null=True, blank=True)
    gender = models.CharField(choices=GENDER,max_length=10,null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    profile = models.ImageField(upload_to='profile_pic', default='default.jpg', null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        
        return str(self.user)
class EventType(models.Model):
    name = models.CharField(max_length=100) 
    
    
    def __str__(self):
        
        return self.name
    
    
class Event(models.Model):
   
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    time = models.TimeField()
    card = models.ImageField(upload_to='cards' , null=True, blank=True)
    qrcode = models.ImageField(upload_to='eventqrcode' , null=True, blank=True)
    eventtype = models.ForeignKey(EventType, on_delete=models.CASCADE)
    user = models.ForeignKey(Admins,on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.name
    def save(self,*args,**kwargs):
      qrcode_img=qrcode.make(self.name)
      canvas=Image.new("RGB", (300,300),"white")
      draw=ImageDraw.Draw(canvas)
      canvas.paste(qrcode_img)
      buffer=BytesIO()
      canvas.save(buffer,"PNG")
      self.qrcode.save(f'{self.id}.png',File(buffer),save=False)
      canvas.close()
      super().save(*args,**kwargs)
    
    



class Guest(models.Model):
    
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    
    def __str__(self):
        
        return self.fullname