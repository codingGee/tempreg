from re import M
from tabnanny import verbose
from django.db import models
from django.conf import settings

class Profile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  phone = models.IntegerField(default=0)
  city = models.CharField(max_length=100, default='')
  date_of_birth = models.DateField(blank=True, null=True)
  photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  
  class Meta:
      verbose_name_plural = 'profile'
  
  def __str__(self):
    return f'Profile for user {self.user.username}'
  
  
class Gallery(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  front_image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  left_side = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  back_image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  right_side = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  
  class Meta:
      verbose_name_plural = 'gallery'
  
  def __str__(self):
    return self.user.username 
  
class Car(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  model = models.CharField(max_length=200)
  vin = models.CharField(max_length=200)
  year = models.CharField(max_length=5)
  photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  
  class Meta:
    verbose_name_plural = 'car'
  
  def __str__(self):
    return self.name
  
  