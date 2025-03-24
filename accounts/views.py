from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import random


PROFILE_IMAGES = [
    "https://i.pinimg.com/736x/b1/18/7a/b1187a7c9927df9a85f99d9463d38f30.jpg",
    "https://i.pinimg.com/736x/7d/03/05/7d03058deeafbc58a2bf6b27212ade78.jpg",
    "https://i.pinimg.com/736x/d3/3b/ae/d33baeb31534860aa2752242f59ed9b7.jpg",
    "https://i.pinimg.com/736x/94/2b/72/942b726c6d18577ae7535d229c1e4171.jpg",
    "https://i.pinimg.com/736x/fa/3a/c7/fa3ac79f3d665e9ba368a13b8aba8c34.jpg",
]


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login berhasil!")
            request.session["profile_image"] = random.choice(PROFILE_IMAGES)
            return redirect("home")  # Ganti dengan halaman tujuan setelah login
        else:
            messages.error(request, "Username atau password salah.")

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logout berhasil!")
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username sudah digunakan!")
            else:
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, "Akun berhasil dibuat! Silakan login.")
                return redirect("login")
        else:
            messages.error(request, "Password tidak cocok!")

    return render(request, "accounts/register.html")
