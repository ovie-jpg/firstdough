from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.contrib import messages
from shop.models import Profile
import uuid

# Create your views here.

def register(request, **kwargs):
    if request.method == 'POST':
        ref_by= str(kwargs.get('ref_by'))
        code= str(uuid.uuid4()).replace("-", "")[:5]
        username= request.POST['username']
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        password1= request.POST['password1']
        password2= request.POST['password2']
        telephone= request.POST['telephone']
        email= request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
            elif Profile.objects.filter(code= ref_by).exists():
                user= User.objects.create_user(username= username, first_name= first_name, last_name= last_name, password= password1, email= email)
                ref_profile= Profile.objects.get(code= ref_by)
                ref_user= User.objects.get(username= ref_profile.name)
                ref_profile.recommendations.add(user)
                profile= Profile.objects.create(user= user, name= user.username, code= code, email= user.email, telephone= telephone, rec_by= ref_user)
                user.save()
                ref_profile.save()
                profile.save()
                return redirect(reverse('signin'))
            else:
                user= User.objects.create_user(username= username, first_name= first_name, last_name= last_name, password= password1, email= email)
                profile= Profile.objects.create(user= user, name= user.username, code= code, email= user.email, telephone= telephone)
                user.save()
                profile.save()
                return redirect(reverse('signin'))
        else:
            messages.info(request, 'password not matching')
    return render(request, 'register.html')

def custom_login(request, **kwargs):
    if request.method == 'POST':
        ref_by= str(kwargs.get('ref_by'))
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if Profile.objects.filter(user=user).exists():
            profile= Profile.objects.get(user=user)
        if user is not None:
            if Profile.objects.filter(code=ref_by).exists() and profile.rec_by == None:
                ref_profile= Profile.objects.get(code=ref_by)
                profile.rec_by= ref_profile.user
                ref_profile.recommendations.add(user)
                profile.save()
                ref_profile.save()
                auth.login(request, user)
                return redirect('home')
            else:
                auth.login(request, user)
                return redirect('home')
        else:
            messages.info(request, 'invalid details')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')