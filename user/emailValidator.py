import requests
from django.conf import settings


def check_email_with_abstract(email):
    """
    Check if email is REAL using Abstract Email Reputation API
    Returns: (is_valid, message)
    """
    api_key = settings.ABSTRACT_API_KEY

    url = f"https://emailreputation.abstractapi.com/v1/?api_key={api_key}&email={email}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if 'error' in data:
            return False, "Email verification failed. Please try again."

        # Get deliverability status
        deliverability = data.get('email_deliverability', {})
        status = deliverability.get('status', '')

        # Only accept deliverable emails
        if status == 'deliverable':
            return True, "Email is valid"
        else:
            return False, "This email does not exist. Please use a real email."

    except Exception as e:
        print(f"API Error: {str(e)}")
        return False, "Email verification service is temporarily unavailable. Please try again."