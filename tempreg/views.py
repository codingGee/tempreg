from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from django.db.models import Q 
from django.contrib.auth.models import User
from .models import Gallery, Profile
from .forms import CarPhoto, LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required

# login view 
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenicated Successful')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'signin.html', {'form': form})

# dashboard view 
@login_required
def dashboard(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
        args = {'user': user}
    return render(request, 'dashboard.html', args)


# register view 
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object 
            new_user = user_form.save(commit=False)
            # set the choosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # save the user object 
            new_user.save()
            # Create the User Profile 
            Profile.objects.create(user = new_user)
            return render(request, 'sign_up_done.html', { 'new_user' : new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'signup.html', {'user_form': user_form})

# edit view 
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance= request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated sucessful')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'edit.html', {'user_form': user_form, 'profile_form':profile_form})

# gallery view 
def gallery(request):
    if request.method == "POST":
        gallery_form = CarPhoto(request.POST, request.FILES)
        if gallery_form.is_valid():
            gallery_form.save()
            messages.success(request, 'Image upload sucessful')
        else:
            messages.error(request, 'Error uploading your imagee')
    else:
        gallery_form = CarPhoto()
    return render(request, 'car_image.html', {'gallery_form':gallery_form})


# view images from galler 
def gallery_view(request):
    if request.method == 'GET':
        # getting all the objects of gallery
        car_image = Gallery.objects.all()
        return render(request, 'car_image_view.html', {'car_image' : car_image})
    
# search view 
class SearchResultsView(ListView):
    model = User
    template_name = 'search.html'

    def get_queryset(self): # new
        query = self.request.GET.get('q')
        object_list = User.objects.filter(
            Q(username=query) | Q(email=query)
        )
        return object_list