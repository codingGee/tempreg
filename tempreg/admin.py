from django.contrib import admin
from .models import Gallery, Profile, Car

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'phone', 'state', 'city']
    
@admin.register(Gallery)
class CarImage(admin.ModelAdmin):
    list_display = ['user', 'front_image', 'left_side', 'back_image', 'right_side']
    
@admin.register(Car)
class Cars(admin.ModelAdmin):
    list_display = ['user','name', 'model', 'vin', 'year', 'photo']