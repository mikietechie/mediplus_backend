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
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_view = dict(request.GET).get("next", "index")
            return HttpResponseRedirect(reverse(next))
        else:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "app/login.html")

@login_required(login_url="/login")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        next_view = dict(request.GET).get("next", "index")
        return HttpResponseRedirect(reverse(next))
    else:
        return render(request, "app/register.html")

