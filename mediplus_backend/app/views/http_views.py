from django.shortcuts import render, reverse, redirect
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
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
from app.utilities import (
    clean_filters,
    get_and_pop_from_dict
)
from django.db import IntegrityError
from app.forms import UserForm


def index_view(request): return render(request, "app/index.html", dict(company = Company.objects.first()))

def contact_view(request): return render(request, "app/contact.html", dict(company = Company.objects.first()))

def about_view(request): return render(request, "app/about.html", dict(company = Company.objects.first()))

def categories_view(request): return render(request, "app/categories.html", dict(company = Company.objects.first()))

def brands_view(request): return render(request, "app/brands.html", dict(company = Company.objects.first()))

def products_view(request):
    filters = clean_filters(request.GET)
    page = get_and_pop_from_dict(filters, "page")
    per_page = get_and_pop_from_dict(filters, "per_page") or 24
    for (k, v) in [i for i in filters.items()]:
        if not v: filters.pop(k)
    products_query_set = Product.objects.filter(**filters)
    paginator = Paginator(products_query_set, per_page=per_page)
    page = paginator.get_page(page)
    return render(request, "app/products.html", dict(
        company = Company.objects.first(),
        page = page,
        paginator = paginator
    ))

def product_view(request, pk):
    return render(request, "app/product.html", dict(
        company = Company.objects.first(),
        product = Product.objects.get(pk=pk)
    ))

@login_required(login_url="/login")
def account_view(request): return render(request, "app/account.html", dict(company = Company.objects.first()))

#### AUTHENTICATION VIEWS ####
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
        except:
            return render(request, "app/login.html", {
                "message": "Invalid username and/or password."
            })
        user = authenticate(request, username=user.username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_view = request.GET.get("next", "/")
            return HttpResponseRedirect(next_view)
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
        password_confirmation = request.POST.get("confirm-password")
        if password != password_confirmation:
            return render(request, "app/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user_form = UserForm(request.POST)
            if not user_form.is_valid():
                return render(request, "app/register.html", {
                    "message": "Invalid data."
                })
            user = user_form.save()
            user.set_password(password)
            user.save()
        except IntegrityError:
            return render(request, "app/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        next_view = dict(request.GET).get("next", "/")
        return HttpResponseRedirect(next_view)
    return render(request, "app/register.html")

