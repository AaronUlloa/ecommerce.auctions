from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import AuctionItem, ItemImage
from .forms import AuctionItemForm, ItemImageForm

# from .models import AuctionItem, Category, Comment, Like, Bid, Cart, Purchase, ItemImage

# Create your views here.


def item_list(request):
    items = AuctionItem.objects.filter(is_active=True)
    return render(
        request, "view/item_list.html", {"title": f"Articulos Activos", "items": items}
    )


@login_required
def create_item(request):
    if request.method == "POST":
        item_form = AuctionItemForm(request.POST)
        image_form = ItemImageForm(request.POST, request.FILES)
        if item_form.is_valid() and image_form.is_valid():
            item = item_form.save(commit=False)
            item.seller = request.user
            item.save()

            for image in request.FILES.getlist("images"):
                item_image = ItemImage(item=item, image=image)
                item_image.save()

            return redirect("auctions:item_detail", item_id=item.id)
    else:
        item_form = AuctionItemForm()
        image_form = ItemImageForm()
    return render(
        request,
        "view/create_item.html",
        {"item_form": item_form, "image_form": image_form},
    )


# @login_required
# def add_comment(request, item_id):
#     item = AuctionItem.objects.get(pk=item_id)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.item = item
#             comment.user = request.user
#             comment.save()
#             return redirect("auctions:item_detail", item_id=item.id)
#     else:
#         form = CommentForm()
#     return render(request, "view/add_comment.html", {"form": form, "item": item})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:item_list"))
        else:
            return render(
                request,
                "auth/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auth/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:item_list"))


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
        return HttpResponseRedirect(reverse("auctions:item_list"))
    else:
        return render(
            request, "auth/register.html", {"title": "Registrate ahora en BidHub"}
        )


def forget(request):
    return render(request, "auth/forget.html")
