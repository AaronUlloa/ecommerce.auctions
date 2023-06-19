from django.contrib import admin
from .models import (
    Bid,
    User,
    Like,
    Cart,
    Comment,
    Category,
    Purchase,
    ItemImage,
    AuctionItem,
)

# Register your models here.

admin.site.register(
    [Category, AuctionItem, ItemImage, Purchase, Comment, Cart, Like, User, Bid]
)
