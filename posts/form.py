from django import forms

from posts.models import Post, PostImage


class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = [
                'price',
                'type',
                'category',
                'description',
                'quantity',
            ]

            widgets = {
                'price': forms.NumberInput(attrs={
                        'min': 1,
                        'placeholder': 'Enter price'
                    }
                ),

                'quantity': forms.NumberInput(attrs={
                    'min': 1,
                    'placeholder': 'Enter quantity'
                }
                )
            }

            def validate_price(self):
                price = self.cleaned_data.get('price')

                if price <= 0:
                    raise forms.ValidationError(
                        "Price must be greater than 0."
                    )

                return price

            def validate_quantity(self):
                quantity = self.cleaned_data.get('quantity')

                if quantity <= 0:
                    raise forms.ValidationError(
                        "quantity must be greater than 0."
                    )

                return quantity

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = [
            'image'
        ]