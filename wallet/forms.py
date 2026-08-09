from django import forms
from django.core.validators import RegexValidator
from PIL import Image
import re

from .models import DepositRequest, WithdrawRequest


# =========================================================
# PHONE VALIDATOR
# 09 + 6 to 9 additional digits
# Total: 8 to 11 digits
# Examples:
# 09123456
# 091234567
# 09123456789
# =========================================================

phone_validator = RegexValidator(
    regex=r"^09\d{6,9}$",
    message="Phone number must start with 09 and contain 8 to 11 digits.",
    code="invalid_phone",
)


# =========================================================
# DEPOSIT FORM
# =========================================================

class DepositForm(forms.ModelForm):

    # -----------------------------------------------------
    # PHONE FIELD
    # -----------------------------------------------------

    sender_phone = forms.CharField(
        min_length=8,
        max_length=11,
        required=True,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control modern-input",
                "placeholder": "09XXXXXXXXX",
                "inputmode": "numeric",
                "autocomplete": "tel",
                "pattern": r"09\d{6,9}",
                "maxlength": "11",
            }
        ),
    )

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
                    "class": "form-select modern-input",
                }
            ),

            "sender_name": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Sender Name",
                }
            ),

            "transaction_id": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Transaction ID",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Enter deposit amount",
                    "min": "1000",
                    "step": "1",
                }
            ),

            "screenshot": forms.ClearableFileInput(
                attrs={
                    "class": "form-control modern-input",
                    "accept": "image/jpeg,image/png",
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "class": "form-control modern-input",
                    "rows": 4,
                    "placeholder": "Optional note...",
                }
            ),
        }

    # -----------------------------------------------------
    # SENDER PHONE
    # -----------------------------------------------------

    def clean_sender_phone(self):

        phone = self.cleaned_data.get("sender_phone", "").strip()

        if not re.fullmatch(r"09\d{6,9}", phone):

            raise forms.ValidationError(
                "Enter a valid Myanmar phone number starting with 09 and containing 8 to 11 digits."
            )

        return phone

    # -----------------------------------------------------
    # AMOUNT
    # -----------------------------------------------------

    def clean_amount(self):

        amount = self.cleaned_data.get("amount")

        if amount is None:

            raise forms.ValidationError(
                "Please enter the deposit amount."
            )

        if amount < 1000:

            raise forms.ValidationError(
                "Minimum deposit amount is MMK 1,000."
            )

        return amount

    # -----------------------------------------------------
    # SCREENSHOT
    # -----------------------------------------------------

    def clean_screenshot(self):

        image = self.cleaned_data.get("screenshot")

        if not image:

            raise forms.ValidationError(
                "Please upload your payment screenshot."
            )

        # Maximum 5 MB
        if image.size > 5 * 1024 * 1024:

            raise forms.ValidationError(
                "Screenshot must be smaller than 5 MB."
            )

        # Allowed MIME types
        allowed = [
            "image/jpeg",
            "image/png",
        ]

        if image.content_type not in allowed:

            raise forms.ValidationError(
                "Only JPG and PNG images are allowed."
            )

        # Check actual image
        try:

            img = Image.open(image)

            img.verify()

        except Exception:

            raise forms.ValidationError(
                "The uploaded file is not a valid image."
            )

        # Re-open image after verify()
        image.seek(0)

        img = Image.open(image)

        # Minimum resolution
        if img.width < 500 or img.height < 500:

            raise forms.ValidationError(
                "Image resolution is too low. Please upload a clearer screenshot."
            )

        image.seek(0)

        return image

    # -----------------------------------------------------
    # TRANSACTION ID
    # -----------------------------------------------------

    def clean_transaction_id(self):

        tx = self.cleaned_data.get("transaction_id", "").strip()

        if not tx:

            raise forms.ValidationError(
                "Please enter the transaction ID."
            )

        if DepositRequest.objects.filter(
            transaction_id=tx
        ).exists():

            raise forms.ValidationError(
                "Transaction ID already exists."
            )

        return tx


# =========================================================
# WITHDRAW FORM
# =========================================================

class WithdrawForm(forms.ModelForm):

    # -----------------------------------------------------
    # PHONE FIELD
    # -----------------------------------------------------

    receiver_phone = forms.CharField(
        min_length=8,
        max_length=11,
        required=True,
        validators=[phone_validator],
        widget=forms.TextInput(
            attrs={
                "class": "form-control modern-input",
                "placeholder": "09XXXXXXXXX",
                "inputmode": "numeric",
                "autocomplete": "tel",
                "pattern": r"09\d{6,9}",
                "maxlength": "11",
            }
        ),
    )

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
                    "class": "form-select modern-input",
                }
            ),

            "receiver_name": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Receiver Name",
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Minimum MMK 1,000",
                    "min": "1000",
                    "step": "1",
                }
            ),

            "note": forms.Textarea(
                attrs={
                    "class": "form-control modern-input",
                    "rows": 3,
                    "placeholder": "Optional note...",
                }
            ),
        }

    # -----------------------------------------------------
    # RECEIVER NAME
    # -----------------------------------------------------

    def clean_receiver_name(self):

        name = self.cleaned_data.get(
            "receiver_name",
            ""
        ).strip()

        if len(name) < 3:

            raise forms.ValidationError(
                "Receiver name must contain at least 3 characters."
            )

        return name

    # -----------------------------------------------------
    # RECEIVER PHONE
    # -----------------------------------------------------

    def clean_receiver_phone(self):

        phone = self.cleaned_data.get(
            "receiver_phone",
            ""
        ).strip()

        if not re.fullmatch(
            r"09\d{6,9}",
            phone
        ):

            raise forms.ValidationError(
                "Enter a valid Myanmar phone number starting with 09 and containing 8 to 11 digits."
            )

        return phone

    # -----------------------------------------------------
    # AMOUNT
    # -----------------------------------------------------

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