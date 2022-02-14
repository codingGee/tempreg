
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "tempreg"

urlpatterns = [
    #post views 
    path('dashboard', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
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
    path('edit/', views.edit, name='edit'),
    # car gallery
    path('gallery', views.gallery, name='gallery'),
    path('car_images', views.gallery_view, name="car_images" ),
    # seach path 
    path('search/', views.SearchResultsView.as_view(), name='search')
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)