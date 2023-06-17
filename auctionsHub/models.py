from django.db import models
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )

    def __str__(self):
        return self.title


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="images")
    image = CloudinaryField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        folder="photo/",
    )

    def __str__(self):
        return f"Image #{self.pk} - {self.item.title}"


class Auction(models.Model):
    items = models.ManyToManyField(Item, related_name="auctions")
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_auctions"
    )
    is_active = models.BooleanField(default=True)
    bidders = models.ManyToManyField(
        User, through="Bid", related_name="bidded_auctions"
    )

    def __str__(self):
        return f"Auction #{self.pk}"


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid #{self.pk} - Item: {self.auction.pk}, User: {self.bidder.username}"


class Comment(models.Model):
    items = models.ManyToManyField(Item, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        item_comment = [item.title for item in self.items.all()]
        return f"User: {self.user.username} Comment to {', '.join(item_comment)}"


class Like(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Like item: {self.auction.pk}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(Item, related_name="carts")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        item_titles = [item.title for item in self.items.all()]
        return f"Cart #{self.pk} - User: {self.user.username} -Items: {', '.join(item_titles)}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"
