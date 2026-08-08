from django import forms
from .models import DepositRequest, WithdrawRequest
from PIL import Image
import re


class DepositForm(forms.ModelForm):

    class Meta:

        model = DepositRequest

        fields = [
            "payment_method",
            "sender_name",
            "sender_phone",
            "transaction_id",
            "amount",
            "screenshot",
            "note",
        ]

        widgets = {

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select modern-input"
                }
            ),

            "sender_name": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Sender Name"
                }
            ),

            "sender_phone": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "09xxxxxxxxx"
                }
            ),

            "transaction_id": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Transaction ID"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Enter deposit amount"
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "class": "form-control modern-input",
                    "rows": 4,
                    "placeholder": "Optional note..."
                }
            ),
        }

    def clean_sender_phone(self):

        phone = self.cleaned_data["sender_phone"]

        if not phone.startswith("09"):
            raise forms.ValidationError(
                "Phone number must start with 09."
            )

        if len(phone) < 9 or len(phone) > 11:
            raise forms.ValidationError(
                "Enter a valid Myanmar phone number."
            )

        return phone

    def clean_amount(self):

        amount = self.cleaned_data["amount"]

        if amount < 1000:
            raise forms.ValidationError(
                "Minimum deposit amount is MMK 1,000."
            )

        return amount

    def clean_screenshot(self):

        image = self.cleaned_data.get("screenshot")

        if not image:
            raise forms.ValidationError(
                "Please upload your payment screenshot."
            )

        if image.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "Screenshot must be smaller than 5 MB."
            )

        allowed = [
            "image/jpeg",
            "image/png",
        ]

        if image.content_type not in allowed:
            raise forms.ValidationError(
                "Only JPG and PNG images are allowed."
            )

        # Check image dimensions
        img = Image.open(image)

        if img.width < 500 or img.height < 500:
            raise forms.ValidationError(
                "Image resolution is too low. Please upload a clearer screenshot."
            )

        return image

    def clean_transaction_id(self):

        tx = self.cleaned_data["transaction_id"]

        if DepositRequest.objects.filter(transaction_id=tx).exists():
            raise forms.ValidationError(
                "Transaction ID already exists."
            )

        return tx



class WithdrawForm(forms.ModelForm):

    class Meta:

        model = WithdrawRequest

        fields = [
            "payment_method",
            "receiver_name",
            "receiver_phone",
            "amount",
            "note",
        ]

        widgets = {

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "receiver_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Receiver Name"
                }
            ),

            "receiver_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "09xxxxxxxxx"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Minimum MMK 1,000"
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional note..."
                }
            ),
        }

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        if amount is None:
            raise forms.ValidationError(
                "Please enter the withdrawal amount."
            )

        if amount < 1000:
            raise forms.ValidationError(
                "The minimum withdrawal amount is MMK 1,000."
            )

        return amount

    def clean_receiver_name(self):

        name = self.cleaned_data.get("receiver_name")

        if len(name.strip()) < 3:
            raise forms.ValidationError(
                "Receiver name must contain at least 3 characters."
            )

        return name

    def clean_receiver_phone(self):

        phone = self.cleaned_data.get("receiver_phone")

        if not phone.startswith("09"):
            raise forms.ValidationError(
                "Phone number must start with 09."
            )


    def clean_receiver_phone(self):

        phone = self.cleaned_data.get("receiver_phone").strip()

        if not re.fullmatch(r"09\d{9}", phone):
            raise forms.ValidationError(
                "Enter a valid Myanmar phone number (e.g. 09123456789)."
            )

        return phone