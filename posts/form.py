from django import forms

from .models import (
    Post,
    Item,
    SizeVariant,
    ItemImage,
    Category,
)


# ============================================================
# POST FORM
# ============================================================

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            'condition',
            'category',
            'description',
        ]

        widgets = {
            'condition': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'conditionSelect',
                }
            ),

            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'categorySelect',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'postDescription',
                    'rows': 5,
                    'placeholder': (
                        'Describe your post clearly...'
                    ),
                }
            ),
        }

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if not description or not description.strip():
            raise forms.ValidationError(
                'Post description is required.'
            )

        description = description.strip()

        if len(description) < 5:
            raise forms.ValidationError(
                'Post description must contain at least 5 characters.'
            )

        return description


# ============================================================
# ITEM FORM
# ============================================================

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = [
            'name',
            'description',
            'price',
            'simple_quantity',
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter item name',
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': (
                        'Describe this item...'
                    ),
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'step': '1',
                    'placeholder': 'Enter price',
                }
            ),

            'simple_quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'step': '1',
                    'placeholder': 'Enter quantity',
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name or not name.strip():
            raise forms.ValidationError(
                'Item name is required.'
            )

        return name.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')

        if not description or not description.strip():
            raise forms.ValidationError(
                'Item description is required.'
            )

        description = description.strip()

        if len(description) < 5:
            raise forms.ValidationError(
                'Item description must contain at least 5 characters.'
            )

        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None:
            raise forms.ValidationError(
                'Item price is required.'
            )

        if price <= 0:
            raise forms.ValidationError(
                'Item price must be greater than 0.'
            )

        return price

    def clean_simple_quantity(self):
        quantity = self.cleaned_data.get('simple_quantity')

        if quantity is None:
            raise forms.ValidationError(
                'Quantity is required.'
            )

        if quantity <= 0:
            raise forms.ValidationError(
                'Quantity must be greater than 0.'
            )

        return quantity


# ============================================================
# SIZE VARIANT FORM
# ============================================================

class SizeVariantForm(forms.ModelForm):

    class Meta:
        model = SizeVariant

        fields = [
            'size',
            'quantity',
            'price',
        ]

        widgets = {
            'size': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Size',
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'step': '1',
                    'placeholder': 'Quantity',
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '1',
                    'step': '1',
                    'placeholder': 'Price',
                }
            ),
        }

    def clean_size(self):
        size = self.cleaned_data.get('size')

        if not size or not str(size).strip():
            raise forms.ValidationError(
                'Size is required.'
            )

        return str(size).strip()

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')

        if quantity is None:
            raise forms.ValidationError(
                'Quantity is required.'
            )

        if quantity <= 0:
            raise forms.ValidationError(
                'Quantity must be greater than 0.'
            )

        return quantity

    def clean_price(self):
        price = self.cleaned_data.get('price')

        if price is None:
            raise forms.ValidationError(
                'Price is required.'
            )

        if price <= 0:
            raise forms.ValidationError(
                'Price must be greater than 0.'
            )

        return price


# ============================================================
# ITEM IMAGE FORM
# ============================================================

class ItemImageForm(forms.ModelForm):

    class Meta:
        model = ItemImage

        fields = [
            'image',
        ]

        widgets = {
            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': 'image/*',
                }
            ),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise forms.ValidationError(
                'Please select an image.'
            )

        return image