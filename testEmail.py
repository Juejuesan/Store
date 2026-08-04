import requests

# Your API key
API_KEY = '867d312f8b184d068fd974717522cd61'

# Test these emails
test_emails = [
    'yelminaung816@gmail.com',  # Your real email
    'test@gmail.com',  # Should be real
    'tes223334444@gmail.com',  # Should be fake
    'fakeemail123456@xyzabc.com',  # Should be fake
]

print("=" * 60)
print("TESTING ABSTRACT EMAIL REPUTATION API")
print("=" * 60)

for email in test_emails:
    url = f"https://emailreputation.abstractapi.com/v1/?api_key={API_KEY}&email={email}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Get important fields
        deliverability = data.get('email_deliverability', {})
        status = deliverability.get('status', 'unknown')
        is_format_valid = deliverability.get('is_format_valid', False)
        is_smtp_valid = deliverability.get('is_smtp_valid', False)

        quality = data.get('email_quality', {})
        score = quality.get('score', 0)
        is_disposable = quality.get('is_disposable', False)

        risk = data.get('email_risk', {})
        address_risk = risk.get('address_risk_status', 'unknown')

        print(f"\n{'=' * 60}")
        print(f"Email: {email}")
        print(f"{'=' * 60}")
        print(f"  Status: {status}")
        print(f"  Format Valid: {is_format_valid}")
        print(f"  SMTP Valid: {is_smtp_valid}")
        print(f"  Quality Score: {score}")
        print(f"  Is Disposable: {is_disposable}")
        print(f"  Risk Level: {address_risk}")

        # Decision
        if status == 'deliverable':
            print(f"  ✅ RESULT: REAL EMAIL - Accept registration")
        elif status == 'undeliverable':
            print(f"  ❌ RESULT: FAKE EMAIL - Block registration")
        else:
            print(f"  ⚠️  RESULT: UNKNOWN - Block registration")

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)