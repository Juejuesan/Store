from django.core.validators import validate_email
from django.core.exceptions import ValidationError


def check_email_with_abstract(email):

    try:
        validate_email(email)

        return True, "Email format is valid."

    except ValidationError:

        return False, "Please enter a valid email address."