from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.forms import RegistrationUserForm


def index_view(request):
    context = {}
    return render(request, "index.html", context)

def room_view(request, room_name):
    user = request.user
    return render(request, "room.html", {"room_name": room_name, "user": user})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        pwd = request.POST.get("pwd")
        user = authenticate(request, email=email, password=pwd)

        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Wrong email or password..")

    context = {

    }
    return render(request, "login.html", context)

def register_view(request):

    form = RegistrationUserForm()
    if request.method == 'POST':
        form = RegistrationUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password1"))
            new_user.is_active = True
            new_user.save()
            return redirect("login")
        else:
            print(form.errors)
    context = {
        "form": form,
    }
    return render(request, 'register.html',context)

