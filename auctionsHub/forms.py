from django import forms
from django.utils.regex_helper import Choice
from .models import AuctionItem, Comment, Bid, ItemImage, Category
import cloudinary
import cloudinary.uploader
from multiupload.fields import MultiFileField


class AuctionItemForm(forms.ModelForm):
    title = forms.CharField(
        label="Título",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "forms__input"}),
    )
    description = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(attrs={"rows": 4, "class": "forms__input"}),
    )
    category = forms.ModelChoiceField(
        label="Categoría",
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "forms__input"}),
    )
    starting_price = forms.DecimalField(
        label="Precio de inicio",
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={"class": "forms__input"}),
    )
    current_price = forms.DecimalField(
        label="Precio Actual",
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={"class": "forms__input"}),
    )

    class Meta:
        model = AuctionItem
        fields = ("title", "description", "category", "starting_price", "current_price")


class CommentForm(forms.ModelForm):
    text = forms.CharField(label="Comentario", widget=forms.Textarea(attrs={"rows": 4}))

    class Meta:
        model = Comment
        fields = ("text",)


class BidForm(forms.ModelForm):
    price = forms.DecimalField(
        label="Precio de oferta", max_digits=10, decimal_places=2
    )

    class Meta:
        model = Bid
        fields = ("price",)


class ItemImageForm(forms.ModelForm):
    images = MultiFileField(
        min_num=1,
        max_num=5,
        max_file_size=1024 * 1024 * 5,
        required=True,
    )

    class Meta:
        model = ItemImage
        fields = ("images",)

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Guardar las imágenes en Cloudinary
        uploaded_images = []
        for image in self.cleaned_data["images"]:
            uploaded_image = cloudinary.uploader.upload(image)
            uploaded_images.append(uploaded_image["secure_url"])

        # Guardar los enlaces de las imágenes en el modelo ItemImage
        instance.images = uploaded_images

        if commit:
            instance.save()
        return instance


class CustomClearableFileInput(forms.ClearableFileInput):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.setdefault("attrs", {})
        attrs["class"] = "form-control-file custom-class"
        super().__init__(*args, **kwargs)
