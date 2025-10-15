#!/usr/bin/env python3
"""Help find the correct secret key format."""
import hashlib
import hmac
import base64
import json
import sys

def test_signature(secret, label):
    """Test if this secret produces the correct signature."""
    body = json.dumps({"pageNo": "1", "pageSize": "10"}, separators=(',', ':'))

    # Generate MD5
    md5 = hashlib.md5()
    md5.update(body.encode('utf-8'))
    content_md5 = base64.b64encode(md5.digest()).decode('utf-8')

    # Generate signature
    string_to_sign = f"POST\n{content_md5}\napplication/json;charset=UTF-8\nTue, 14 Oct 2025 23:59:05 GMT\n/v1/api/userStationList"

    hmac_obj = hmac.new(
        secret.encode('utf-8') if isinstance(secret, str) else secret,
        msg=string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha1
    )
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')

    expected = "/1IVORZPwp62auEhD5EKSuQ/2yQ="
    match = signature == expected

    print(f"{label:40s} -> {signature:30s} {'✓ MATCH!' if match else '✗'}")
    return match

if len(sys.argv) < 2:
    print("Usage: python3 find_secret.py <secret_key>")
    print("\nThis script will try different encodings of your secret key")
    print("to find which one produces the correct signature.")
    sys.exit(1)

secret_input = sys.argv[1]

print("\n" + "=" * 80)
print("TESTING DIFFERENT SECRET KEY FORMATS")
print("=" * 80)
print(f"\nInput secret: {secret_input}")
print(f"Expected signature: /1IVORZPwp62auEhD5EKSuQ/2yQ=")
print("\nTrying different formats...\n")

# Try different encodings
formats_tested = []

# 1. Plain secret (as-is)
if test_signature(secret_input, "1. Plain secret (as-is)"):
    print("\n✓ Found it! Use the secret as-is (plain text)")
    sys.exit(0)

# 2. Base64 decoded
try:
    decoded_b64 = base64.b64decode(secret_input)
    if test_signature(decoded_b64.decode('utf-8', errors='ignore'), "2. Base64 decoded (UTF-8)"):
        print(f"\n✓ Found it! Your secret is base64-encoded.")
        print(f"Decoded secret: {decoded_b64.decode('utf-8', errors='ignore')}")
        sys.exit(0)
except Exception:
    print("2. Base64 decoded (UTF-8)                -> (decode failed)")

# 3. Hex decoded
try:
    decoded_hex = bytes.fromhex(secret_input)
    if test_signature(decoded_hex.decode('utf-8', errors='ignore'), "3. Hex decoded"):
        print(f"\n✓ Found it! Your secret is hex-encoded.")
        print(f"Decoded secret: {decoded_hex.decode('utf-8', errors='ignore')}")
        sys.exit(0)
except Exception:
    print("3. Hex decoded                           -> (decode failed)")

# 4. Try without whitespace
secret_stripped = secret_input.strip()
if secret_stripped != secret_input:
    if test_signature(secret_stripped, "4. Secret with whitespace removed"):
        print("\n✓ Found it! Your secret had extra whitespace")
        sys.exit(0)

print("\n" + "=" * 80)
print("⚠️  NO MATCH FOUND")
print("=" * 80)
print("\nThe secret key format couldn't be determined.")
print("\nPlease check:")
print("1. Go to Solis Cloud website (www.soliscloud.com)")
print("2. Navigate to API Management")
print("3. Copy the 'API Secret' field")
print("4. Make sure you're copying the SECRET, not the KEY ID")
print("5. The secret is different from the Key ID (1300386381677986852)")
print("\nIf you're using the Solis Cloud API tester, check the 'Secret Key' field.")
print("=" * 80 + "\n")
