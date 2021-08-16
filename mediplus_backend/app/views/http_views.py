from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from app.models import (
    User,
    Brand,
    Category,
    Product,
    Cart,
    CartItem,
    Watch,
    PrescribePermission,
    Company
)


def index_view(request):
    context = {"company": Company.objects.first()}
    return render(request=request, template_name="app/index.html", context=context)


#### AUTHENTICATION VIEWS ####
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_view = dict(request.GET).get("next", "index")
            return HttpResponseRedirect(reverse(next))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, "app/login.html")

@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")
        if password != password_confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User(
                email=request.POST.get("email"),
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                phone=request.POST.get("phone"),
                image=request.POST.get("image"),
                DOB=request.POST.get("DOB"),
                address=request.POST.get("address")
            )
            user.set_password(password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        next_view = dict(request.GET).get("next", "index")
        return HttpResponseRedirect(reverse(next))
    return render(request, "app/register.html")

