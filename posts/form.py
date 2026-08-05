from django import forms
from .models import Post, Item, SizeVariant, ItemImage, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['condition', 'category', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'simple_quantity']

class SizeVariantForm(forms.ModelForm):
    class Meta:
        model = SizeVariant
        fields = ['size', 'quantity']

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']