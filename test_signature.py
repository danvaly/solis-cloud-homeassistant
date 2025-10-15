#!/usr/bin/env python3
"""Test signature generation for Solis Cloud API."""
import hashlib
import hmac
import base64
import json

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

    print("=" * 60)
    print("Signature Generation Details")
    print("=" * 60)
    print(f"verb: {verb}")
    print(f"content_md5: {content_md5}")
    print(f"content_type: {content_type}")
    print(f"date: {date}")
    print(f"resource: {resource}")
    print()
    print("string_to_sign:")
    print(repr(string_to_sign))
    print()

    hmac_obj = hmac.new(
        secret.encode('utf-8'),
        msg=string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha1
    )
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')

    print(f"signature: {signature}")
    print(f"authorization: API {key_id}:{signature}")
    print()

    return f"API {key_id}:{signature}"

# Test with inverterDetail example from your curl
print("\n" + "=" * 60)
print("TEST 1: inverterDetail (from your curl example)")
print("=" * 60)

body1 = json.dumps({"id": "1308675217949702883", "sn": "1033320253070089"})
content_md5_1 = get_content_md5(body1)

print(f"Body: {body1}")
print(f"Content-MD5: {content_md5_1}")
print()

# Expected from your curl:
# content-md5: Rj65esO7Ob/1oA/2DcJDxw==
# time: Tue, 14 Oct 2025 23:27:08 GMT
# authorization: API 1300386381677986852:9NGKBqNLZxmJT9FI14yAqhOchD8=

print("Expected Content-MD5: Rj65esO7Ob/1oA/2DcJDxw==")
print(f"Computed Content-MD5: {content_md5_1}")
print(f"Match: {content_md5_1 == 'Rj65esO7Ob/1oA/2DcJDxw=='}")
print()

# Test signature generation (you'll need to provide your secret)
# generate_signature(
#     "1300386381677986852",
#     "YOUR_SECRET_HERE",
#     "POST",
#     content_md5_1,
#     "application/json",
#     "Tue, 14 Oct 2025 23:27:08 GMT",
#     "/v1/api/inverterDetail"
# )

# Test with userStationList
print("\n" + "=" * 60)
print("TEST 2: userStationList")
print("=" * 60)

body2 = json.dumps({"pageNo": 1, "pageSize": 20})
content_md5_2 = get_content_md5(body2)

print(f"Body: {body2}")
print(f"Content-MD5: {content_md5_2}")
print()

# Uncomment and add your secret to test:
# generate_signature(
#     "YOUR_KEY_ID",
#     "YOUR_SECRET",
#     "POST",
#     content_md5_2,
#     "application/json",
#     "YOUR_GMT_TIME",
#     "/v1/api/userStationList"
# )

print("\n" + "=" * 60)
print("To test with your credentials, uncomment the code above")
print("and replace YOUR_KEY_ID and YOUR_SECRET")
print("=" * 60)
