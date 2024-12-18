from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm
from django.forms.models import model_to_dict
from .forms import CreateUserForm, UpdateUserForm, UpdateProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user_auth = authenticate(request, username=username, password=password)
   
        if user_auth is not None:
            login(request, user_auth)
            return redirect('user_info')
        else:
            messages.error(request, 'username and passward does not match')

    return render(request,'accounts/login.html')
def user_register(request):
    if  request.method == 'POST':
        form = CreateUserForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            form.save()
            messages.success(request, 'Registered successfully!')
            return redirect('home')
        else:
            messages.error(request, 'An error occur during registration')
    else:
        form = CreateUserForm()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)
def user_logout(request):
    logout(request)
    return redirect('home')

def user_update(request):
    if request.method == 'POST':
        obj = Profile.objects.get(user__id = request.user.id)
        user = request.user
        form1 = UpdateUserForm(request.POST or None, instance=user)
        form = UpdateProfileForm(request.POST or None,request.FILES, instance=obj)
     
        if form.is_valid() and form1.is_valid():
            obj.bio = request.POST.get('bio')
            # obj.profile_img = request.FILES['profile_img']
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            form.save()
            form1.save()
            messages.success(request,"successfully updated profile")
            return redirect('home')
        else:
            messages.error(request,"error in update profile")
    else:
        obj = Profile.objects.get(user__id = request.user.id)
        user = request.user
        form1 = UpdateUserForm(request.POST or None, instance=user, initial=model_to_dict(user))
        form = UpdateProfileForm(request.POST or None, instance=obj, initial=model_to_dict(obj))
    context = {'form1':form1, 'form': form}
    return render(request, 'accounts/update_profile.html', context)

@login_required(login_url='login')
def user_info(request):
    pro = request.user.profile.project_set.all()
  
    context = {'profile': Profile, 'pro': pro}

    return render(request, 'accounts/user_info.html', context)