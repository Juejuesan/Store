from django import forms
from django.core.validators import RegexValidator
from PIL import Image

from .models import DepositRequest, WithdrawRequest


# =========================================================
# PHONE VALIDATOR
# =========================================================
# Myanmar phone number:
#
# Must:
#   - Start with 09
#   - Contain 8 to 11 digits total
#
# Examples:
#   09123456
#   091234567
#   0912345678
#   09123456789
#
# Pattern:
#   09 + 6 to 9 additional digits
# =========================================================

phone_validator = RegexValidator(
    regex=r"^09\d{6,9}$",
    message=(
        "Phone number must start with 09 "
        "and contain 8 to 11 digits."
    ),
    code="invalid_phone",
)


# =========================================================
# DEPOSIT FORM
# =========================================================

class DepositForm(forms.ModelForm):
    payment_method = forms.ChoiceField(
        choices=[
            ("", "Choose Payment Method"),
            ("KBZ Pay", "KBZ Pay"),
            ("Wave Pay", "Wave Pay"),
            ("AYA Pay", "AYA Pay"),
            ("CB Pay", "CB Pay"),
        ],
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select modern-input",
            }
        ),
    )

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
# =========================================================
# WITHDRAW FORM
# =========================================================

class WithdrawForm(forms.ModelForm):

    # -----------------------------------------------------
    # RECEIVER PHONE
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

    # -----------------------------------------------------
    # META
    # -----------------------------------------------------

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

            # ---------------------------------------------
            # PAYMENT METHOD
            # ---------------------------------------------

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select modern-input",
                }
            ),

            # ---------------------------------------------
            # RECEIVER NAME
            # ---------------------------------------------

            "receiver_name": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Receiver Name",
                    "autocomplete": "name",
                }
            ),

            # ---------------------------------------------
            # AMOUNT
            # ---------------------------------------------

            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Minimum MMK 1,000",
                    "min": "1000",
                    "step": "1",
                    "inputmode": "decimal",
                }
            ),

            # ---------------------------------------------
            # NOTE
            # ---------------------------------------------

            "note": forms.Textarea(
                attrs={
                    "class": "form-control modern-input",
                    "rows": 3,
                    "placeholder": "Optional note...",
                }
            ),
        }

    # -----------------------------------------------------
    # INITIALIZE
    # -----------------------------------------------------

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["payment_method"].empty_label = "Choose Payment Method"

    # -----------------------------------------------------
    # CLEAN RECEIVER NAME
    # -----------------------------------------------------

    def clean_receiver_name(self):

        name = self.cleaned_data.get(
            "receiver_name",
            ""
        ).strip()

        if not name:

            raise forms.ValidationError(
                "Please enter the receiver name."
            )

        if len(name) < 3:

            raise forms.ValidationError(
                "Receiver name must contain at least 3 characters."
            )

        return name

    # -----------------------------------------------------
    # CLEAN RECEIVER PHONE
    # -----------------------------------------------------

    def clean_receiver_phone(self):

        phone = self.cleaned_data.get(
            "receiver_phone",
            ""
        ).strip()

        if not phone:

            raise forms.ValidationError(
                "Please enter the receiver phone number."
            )

        if not phone.isdigit():

            raise forms.ValidationError(
                "Phone number must contain digits only."
            )

        if not phone.startswith("09"):

            raise forms.ValidationError(
                "Phone number must start with 09."
            )

        if len(phone) < 8 or len(phone) > 11:

            raise forms.ValidationError(
                "Phone number must contain 8 to 11 digits."
            )

        return phone

    # -----------------------------------------------------
    # CLEAN AMOUNT
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