
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "tempreg"

urlpatterns = [
    #private views 
    # start dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/', views.settings_page, name='settings'),
    # change password urls 
    path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done' ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # register url 
    path('register/', views.register, name='register'),
    path('create-profile/', views.create_profile, name='create-profile'),
    path('edit/', views.edit, name='edit'),
    path('car_profile/', views.carProfile, name="car_profile"),
    path('car_edit/', views.carCreate, name="car_edit"),
    # car gallery
    path('gallery', views.gallery, name='gallery'),
    path('car_images', views.gallery_view, name="car_images" ),
    path('payment-wall/', views.payment_wall, name="payment-wall" ),
    path('payment-process/', views.payment_process, name="payment-process" ),
    # seach path 
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('search-state/', views.StateSearchView.as_view(), name='search-state'),
    path('search-state-done/<str:state>/', views.StateSearchDone.as_view(), name='search-state-done'),
    
    # public route
    path('', views.HomeView.as_view(), name="home" ),
    
]
