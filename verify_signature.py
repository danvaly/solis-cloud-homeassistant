#!/usr/bin/env python3
"""Verify signature matches the working curl example."""
import hashlib
import hmac
import base64
import json
import sys

def get_content_md5(body):
    """Generate MD5 hash of the request body."""
    md5 = hashlib.md5()
    md5.update(body.encode('utf-8'))
    return base64.b64encode(md5.digest()).decode('utf-8')

def generate_signature(key_id, secret, verb, content_md5, content_type, date, resource):
    """Generate HMAC-SHA1 signature.
    
    Note: content_type should be "application/json" (without charset)
    for signature generation, even though the actual HTTP header
    uses "application/json;charset=UTF-8".
    """
    string_to_sign = f"{verb}\n{content_md5}\n{content_type}\n{date}\n{resource}"

    print("=" * 70)
    print("SIGNATURE GENERATION TEST")
    print("=" * 70)
    print(f"\nverb: {verb}")
    print(f"content_md5: {content_md5}")
    print(f"content_type: {content_type}")
    print(f"date: {date}")
    print(f"resource: {resource}")
    print(f"\nstring_to_sign:")
    print(repr(string_to_sign))
    print()

    hmac_obj = hmac.new(
        secret.encode('utf-8'),
        msg=string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha1
    )
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')

    authorization = f"API {key_id}:{signature}"

    print(f"Generated signature: {signature}")
    print(f"Authorization header: {authorization}")
    print()

    return signature

if len(sys.argv) < 3:
    print("Usage: python3 verify_signature.py <key_id> <secret>")
    print("\nThis will verify the signature generation against your working curl example.")
    sys.exit(1)

key_id = sys.argv[1]
secret = sys.argv[2]

# Test data from your working curl
body = json.dumps({"pageNo": "1", "pageSize": "10"}, separators=(',', ':'))
content_md5 = get_content_md5(body)
time_str = "Tue, 14 Oct 2025 23:59:05 GMT"

print(f"Body: {body}")
print(f"Computed MD5: {content_md5}")
print(f"Expected MD5: sAGxE9QzeBN88qPrz+sCZQ==")
print(f"MD5 Match: {content_md5 == 'sAGxE9QzeBN88qPrz+sCZQ=='} ✓" if content_md5 == "sAGxE9QzeBN88qPrz+sCZQ==" else "MD5 Match: False ✗")
print()

signature = generate_signature(
    key_id,
    secret,
    "POST",
    content_md5,
    "application/json",
    time_str,
    "/v1/api/userStationList"
)

print("=" * 70)
print("COMPARISON WITH YOUR WORKING CURL")
print("=" * 70)
print(f"Expected signature: /1IVORZPwp62auEhD5EKSuQ/2yQ=")
print(f"Generated signature: {signature}")
print(f"Match: {signature == '/1IVORZPwp62auEhD5EKSuQ/2yQ='} {'✓' if signature == '/1IVORZPwp62auEhD5EKSuQ/2yQ=' else '✗'}")
print()

if signature == "/1IVORZPwp62auEhD5EKSuQ/2yQ=":
    print("✓ SUCCESS! Signature generation is correct!")
    print("The integration should work now.")
else:
    print("✗ MISMATCH! There's still an issue with signature generation.")
    print("This could be due to:")
    print("  - Incorrect secret key")
    print("  - Encoding issues")
    print("  - Different string_to_sign format")

print("=" * 70)
