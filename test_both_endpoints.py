#!/usr/bin/env python3
"""Test both Solis Cloud API endpoints with your working examples."""
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
    """Generate HMAC-SHA1 signature."""
    string_to_sign = f"{verb}\n{content_md5}\n{content_type}\n{date}\n{resource}"

    hmac_obj = hmac.new(
        secret.encode('utf-8'),
        msg=string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha1
    )
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')

    return signature, string_to_sign

if len(sys.argv) < 3:
    print("Usage: python3 test_both_endpoints.py <key_id> <secret>")
    print("\nExample: python3 test_both_endpoints.py 1300386381677986852 'your_secret'")
    sys.exit(1)

key_id = sys.argv[1]
secret = sys.argv[2]

print("\n" + "=" * 80)
print("SOLIS CLOUD API SIGNATURE VERIFICATION")
print("=" * 80)

# Test 1: userStationList
print("\n" + "=" * 80)
print("TEST 1: /v1/api/userStationList")
print("=" * 80)

body1 = json.dumps({"pageNo": "1", "pageSize": "10"}, separators=(',', ':'))
md5_1 = get_content_md5(body1)
time1 = "Tue, 14 Oct 2025 23:59:05 GMT"

print(f"\nRequest Body: {body1}")
print(f"Content-MD5:  {md5_1}")
print(f"Expected MD5: sAGxE9QzeBN88qPrz+sCZQ==")
print(f"MD5 Match:    {'✓ YES' if md5_1 == 'sAGxE9QzeBN88qPrz+sCZQ==' else '✗ NO'}")

sig1, str_to_sign1 = generate_signature(
    key_id, secret, "POST", md5_1,
    "application/json;charset=UTF-8",
    time1,
    "/v1/api/userStationList"
)

print(f"\nString to sign:")
print(repr(str_to_sign1))
print(f"\nGenerated Signature: {sig1}")
print(f"Expected Signature:  /1IVORZPwp62auEhD5EKSuQ/2yQ=")
print(f"Signature Match:     {'✓ YES' if sig1 == '/1IVORZPwp62auEhD5EKSuQ/2yQ=' else '✗ NO'}")
print(f"\nAuthorization: API {key_id}:{sig1}")

# Test 2: inverterDetail
print("\n" + "=" * 80)
print("TEST 2: /v1/api/inverterDetail")
print("=" * 80)

body2 = json.dumps({"id": "1308675217949702883", "sn": "1033320253070089"}, separators=(',', ':'))
md5_2 = get_content_md5(body2)
time2 = "Wed, 15 Oct 2025 00:00:29 GMT"

print(f"\nRequest Body: {body2}")
print(f"Content-MD5:  {md5_2}")
print(f"Expected MD5: Rj65esO7Ob/1oA/2DcJDxw==")
print(f"MD5 Match:    {'✓ YES' if md5_2 == 'Rj65esO7Ob/1oA/2DcJDxw==' else '✗ NO'}")

sig2, str_to_sign2 = generate_signature(
    key_id, secret, "POST", md5_2,
    "application/json;charset=UTF-8",
    time2,
    "/v1/api/inverterDetail"
)

print(f"\nString to sign:")
print(repr(str_to_sign2))
print(f"\nGenerated Signature: {sig2}")
print(f"Expected Signature:  RXi/TLDGBVVeWrRMFwvTGLMaRyk=")
print(f"Signature Match:     {'✓ YES' if sig2 == 'RXi/TLDGBVVeWrRMFwvTGLMaRyk=' else '✗ NO'}")
print(f"\nAuthorization: API {key_id}:{sig2}")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

test1_pass = (md5_1 == 'sAGxE9QzeBN88qPrz+sCZQ==' and sig1 == '/1IVORZPwp62auEhD5EKSuQ/2yQ=')
test2_pass = (md5_2 == 'Rj65esO7Ob/1oA/2DcJDxw==' and sig2 == 'RXi/TLDGBVVeWrRMFwvTGLMaRyk=')

print(f"\nuserStationList: {'✓ PASS' if test1_pass else '✗ FAIL'}")
print(f"inverterDetail:  {'✓ PASS' if test2_pass else '✗ FAIL'}")

if test1_pass and test2_pass:
    print("\n🎉 SUCCESS! Both signatures match perfectly!")
    print("The integration should work correctly now.")
    print("\nNext steps:")
    print("1. Restart Home Assistant")
    print("2. Remove and re-add the Solis Cloud integration")
    print("3. Your sensors should appear!")
else:
    print("\n⚠️  ISSUE DETECTED")
    if not test1_pass:
        print("\nuserStationList signature doesn't match.")
    if not test2_pass:
        print("\ninverterDetail signature doesn't match.")
    print("\nPossible causes:")
    print("- Incorrect secret key")
    print("- Secret key encoding issue")
    print("- Make sure you copied the secret correctly (no extra spaces)")

print("=" * 80 + "\n")
