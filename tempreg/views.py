from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView,  FormView
from django.db.models import Q 
from django.contrib.auth.models import User
from .models import Car, Gallery, Profile, State
from .forms import CarEditForm, CarPhoto, LoginForm, ProfileForm, UserRegistrationForm, UserEditForm, ProfileEditForm, StatesSearchForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings

# import reverse_lazy
from django.urls import reverse_lazy

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
                    messages.success(request, 'Please proceed to create profile')
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


# vehicle edit 
@login_required
def carProfile(request):
    car_info = Car.objects.filter(user=request.user)
    print(car_info)
    return render(request, 'vehicle_profile.html', {'car_info':car_info})

# car create form
@login_required
def carCreate(request):
    if request.method == "POST":
        user_form = CarEditForm(request.POST,request.FILES)
        if user_form.is_valid():
            user_form.instance.user = request.user
            print(user_form.cleaned_data)
            user_form.save()
            messages.success(request, 'Car information updated sucessful')
        else:
            print(user_form.errors)
            messages.error(request, 'Error updating your Car information')
    else:
        user_form = CarEditForm()
    return render(request, 'car_profile.html', {'user_form': user_form})

# settings
@login_required
def settings_page(request):
    return render(request, 'settings.html')

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
            return render(request, 'sign_up_done.html', { 'new_user' : new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'signup.html', {'user_form': user_form})


@login_required
def create_profile(request):
    if request.method == 'POST':
        user_form = ProfileForm(data=request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.instance.user = request.user
            user_form.save()
            
            messages.success(request, 'Profile creation successful')
        else:
            print(user_form.errors)
            # messages.error(request, 'Error creating profile')
    else:
        user_form = ProfileForm()
    return render(request, 'create-profile.html', {'user_form': user_form})

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
        
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form':profile_form})

# gallery view 
@login_required
def gallery(request):
    if request.method == "POST":
        gallery_form = CarPhoto(request.POST, request.FILES)
        if gallery_form.is_valid():
            gallery_form.save()
            messages.success(request, 'Image upload sucessful')
        else:
            messages.error(request, 'Error uploading your imagee')
    else:
        gallery_form = CarPhoto(instance=request.user)
    return render(request, 'create_gallery.html', {'gallery_form':gallery_form})


# view images from galler 
@login_required
def gallery_view(request):
    if request.method == 'GET':
        # getting all the objects of gallery
        car_image = Gallery.objects.filter(user=request.user)
        return render(request, 'view_gallery.html', {'car_image' : car_image})
    
# payment block 
@login_required
def payment_wall(request):
    return render(request, 'payment-wall.html')
@login_required
def payment_process(request):
    return render(request, 'payment-process.html')
# search view 
@method_decorator(login_required, name='dispatch')
class SearchResultsView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'search.html'
    login_url = 'tempreg:login'
    permission_required = 'tempreg.special_status'
    raise_exception = True  # Raise exception when no access instead of redirect
    permission_denied_message = "You are not allowed here."
    
    
    def get_queryset(self): 
        query = self.request.GET.get('q')
        if query == '':
            object_list = ''
        else:
            object_list = User.objects.filter(
                Q(username=query) | Q(email=query)
            )
        return object_list

# public views 
class HomeView(TemplateView):
    template_name = 'index.html'
    success_message = "Please proceed to create Profile"
    
# @method_decorator(login_required, name='dispatch')
class StateSearchView(FormView):
    template_name = 'state_search.html'
    form_class = StatesSearchForm
    
    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        selected_state = None
        states = Profile.state_choices
        # state_selected = 'Abuja'
        def check_state(state_choice):
            for state in states:
                if state_choice is state[1]:
                    return state[0]
        state_selected = 'Rivers'
        print(f'total tempreg users {state_selected} ' + str(Profile.objects.filter(state=check_state(state_selected)).count()))
        
        return super().get(request, *args, **kwargs)
    def form_valid(self, form):
        state = form.cleaned_data['state']
        return redirect(reverse_lazy('tempreg:search-state-done', kwargs={'state':state}))
# @method_decorator(login_required, name='dispatch')
class StateSearchDone(TemplateView):
    template_name = 'state_search_done.html'
    
    def get(self, request, state, *args, **kwargs):
        print(state)
        states = Profile.state_choices
        # state_selected = 'Abuja'
        def check_state(state_choice):
            for state in states:
                if state_choice is state[0]:
                    return state[0]
        state_selected = 'Rivers'
        kwargs['state_info'] = f'total tempreg users {state} ' + str(Profile.objects.filter(state=check_state(state)).count())
        return self.render_to_response(context=kwargs)
    