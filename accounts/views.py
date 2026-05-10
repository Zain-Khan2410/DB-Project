from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("restaurant:home")
    if request.method == "POST":
        username  = request.POST.get("username", "").strip()
        email     = request.POST.get("email", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        role      = request.POST.get("role", "customer")
        phone     = request.POST.get("phone", "").strip()
        address   = request.POST.get("address", "").strip()

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password1,
                role=role, phone=phone, address=address
            )
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect("restaurant:home")
    return render(request, "accounts/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("restaurant:home")
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get("next", "restaurant:home"))
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "accounts/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@login_required
def profile_view(request):
    if request.method == "POST":
        user         = request.user
        user.phone   = request.POST.get("phone", user.phone)
        user.address = request.POST.get("address", user.address)
        user.email   = request.POST.get("email", user.email)
        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES["profile_pic"]
        user.save()
        messages.success(request, "Profile updated!")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html")
