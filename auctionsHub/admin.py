from django.contrib import admin
from .models import (
    User,
    Category,
    Bid,
    Item,
    Like,
    Cart,
    Order,
    Auction,
    Comment,
    ItemImage,
)

# Register your models here.

admin.site.register(
    [User, ItemImage, Comment, Auction, Order, Cart, Like, Item, Bid, Category]
)
