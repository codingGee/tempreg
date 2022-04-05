from django.db import models
from django.conf import settings

class Profile(models.Model):
  state_choices = (
        ('FC', 'Abuja'),
        ('AB', 'Abia'),
        ('AD', 'Adamawa'),
        ('AK', 'Akwa Ibom'),
        ('AN', 'Anambra'),
        ('BA', 'Bauchi'),
        ('BY', 'Bayelsa'),
        ('BE', 'Benue'),
        ('BO', 'Borno'),
        ('CR', 'Cross River'),
        ('DE', 'Delta'),
        ('EB', 'Ebonyi'),
        ('ED', 'Edo'),
        ('EK', 'Ekiti'),
        ('EN', 'Enugu'),
        ('GO', 'Gombe'),
        ('IM', 'Imo'),
        ('JI', 'Jigawa'),
        ('KD', 'Kaduna'),
        ('KN', 'Kano'),
        ('KT', 'Katsina'),
        ('KE', 'Kebbi'),
        ('KO', 'Kogi'),
        ('KW', 'Kwara'),
        ('LA', 'Lagos'),
        ('NA', 'Nassarawa'),
        ('NI', 'Niger'),
        ('OG', 'Ogun'),
        ('ON', 'Ondo'),
        ('OS', 'Osun'),
        ('OY', 'Oyo'),
        ('PL', 'Plateau'),
        ('RI', 'Rivers'),
        ('SO', 'Sokoto'),
        ('TA', 'Taraba'),
        ('YO', 'Yobe'),
        ('ZA', 'Zamfara')
  )
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  phone = models.PositiveIntegerField()
  state = models.CharField(max_length=20, choices=state_choices)
  city = models.CharField(max_length=20)
  date_of_birth = models.DateField(blank=True, null=True)
  photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
  
  class Meta:
      verbose_name_plural = 'profile'
      permissions = [
      ('special_status', 'Can view user')
    ]
  
  
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
  
class State(models.Model):
  state = models.CharField(max_length=20, choices=Profile.state_choices)
  user_counter = models.IntegerField(default=0)