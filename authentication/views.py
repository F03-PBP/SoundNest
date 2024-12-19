from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('products:home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Login otomatis
            messages.success(request, "Registration successful." )
            return redirect('products:home')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('products:home')


# FLUTTER API
@csrf_exempt
def flutter_login(request: HttpRequest):
    print(request.body)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!",
                "token": token.key,
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)
    
@csrf_exempt
def flutter_register(request):
    print(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        # Check if the passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)
        
        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)
        
        # Create the new user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!",
            "token": token.key,
        }, status=200)
    
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)
    
@csrf_exempt
def flutter_logout(request):
    if request.user.is_authenticated:
        username = request.user.username

        try:
            Token.objects.filter(user=request.user).delete()

            logout(request)  # Logout user
            return JsonResponse({
                "username": username,
                "status": True,
                "message": "Logout berhasil!"
            }, status=200)
        except:
            return JsonResponse({
                "status": False,
                "message": "Logout gagal."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "User tidak terautentikasi."
        }, status=401)
