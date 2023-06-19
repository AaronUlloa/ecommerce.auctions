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


class AuctionItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class ItemImage(models.Model):
#     item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
#     image = CloudinaryField(
#         validators=[
#             FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
#         ],
#         folder="photo/",
#     )


#     def __str__(self):
#         return f"Image #{self.pk} - {self.item.title}"
class ItemImage(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photo/")


class Bid(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(AuctionItem)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
