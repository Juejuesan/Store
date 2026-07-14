from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    model = Post
    from django import forms
    from .models import Post

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = [
                'price',
                'photo',
                'type',
                'category',
                'description',
                'quantity',
            ]

            labels = {
                'price': 'Price',
                'photo': 'Product Image',
                'type': 'Product Type',
                'category': 'Category',
                'description': 'Description',
                'quantity': 'Quantity',
            }

            widgets = {
                'price': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter price'
                }),

                'photo': forms.ClearableFileInput(attrs={
                    'class': 'form-control'
                }),

                'type': forms.Select(attrs={
                    'class': 'form-select'
                }),

                'category': forms.Select(attrs={
                    'class': 'form-select'
                }),

                'description': forms.Textarea(attrs={
                    'class': 'form-control',
                    'placeholder': 'Describe your product...',
                    'rows': 5,
                }),

                'quantity': forms.NumberInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter quantity'
                }),
            }
