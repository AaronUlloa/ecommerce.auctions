from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Category

# Create your views here.


def index(request):
    # activeAuctions = AuctionStatus.objects.filter(is_active=True)
    # imagen = Photo.objects.all()
    # image_url = imagen.url
    # allCategories = Category.objects.all()
    return render(
        request,
        "view/index.html",
        {
            "title": "Publicaciones Activas"
            # "articulos": activeAuctions,
            # "image_url": image_url
            # "categories": allCategories
        },
    )


def addNewItem(request):
    allCategories = Category.objects.all()
    return render(
        request,
        "view/addArticulo.html",
        {"title": f"Publica tu Articulo hoy mismo", "Categories": allCategories},
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(
                request,
                "auth/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auth/login.html", {"title": "Ingresa ahora en BidHub"})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auth/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "auth/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(
            request, "auth/register.html", {"title": "Registrate ahora en BidHub"}
        )


def forget(request):
    return render(request, "auth/forget.html")
