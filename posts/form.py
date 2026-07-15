from django import forms

from posts.models import Post


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

            widgets = {
                'price': forms.NumberInput(attrs={
                        'min': 1,
                        'placeholder': 'Enter price'
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

