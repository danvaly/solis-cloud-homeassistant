# Solis Cloud API Signature Fix Summary

## Date: October 15, 2025

## Overview
Updated the Solis Cloud API implementation to match the official TypeScript example, fixing critical signature generation issues.

## Key Changes

### 1. Content-Type in Signature String
**Issue**: The signature was using `"application/json;charset=UTF-8"` which included the charset parameter.

**Fix**: Changed to use `"application/json"` (without charset) in the signature generation string, while still sending `"application/json;charset=UTF-8"` in the actual HTTP header.

**Rationale**: The TypeScript reference implementation shows that the `contentTypeConstructor` used for signing is `"application/json"` without any charset specification.

### 2. HTTP Header Name Case
**Issue**: Used lowercase `"time"` for the timestamp header.

**Fix**: Changed to capitalized `"Time"` header.

**Rationale**: The TypeScript example explicitly uses `Time` (capital T) as the header name. The documentation notes that browsers don't allow changing the `Date` header, so `Time` must be used instead.

### 3. Simplified Signature Method
**Change**: Removed the `content_type` parameter from `_generate_signature()` method signature. The content type for signature generation is now hardcoded as `"application/json"` inside the method.

**Benefit**: Eliminates confusion and ensures consistency across all API calls.

## Files Modified

### 1. `custom_components/solis_cloud/api.py` ✅
- Updated `_generate_signature()` method to use `"application/json"` internally
- Removed `content_type` parameter from method signature
- Changed all header dictionaries to use `"Time"` (capital T)
- Updated all three API endpoint methods:
  - `get_inverter_data()` (userStationList endpoint)
  - `_get_station_inverters()` (inverterList endpoint)
  - `get_inverter_detail()` (inverterDetail endpoint)

### 2. `test_both_endpoints.py` ✅
- Updated signature generation calls to use `"application/json"` instead of `"application/json;charset=UTF-8"`
- Added docstring comment explaining the content-type difference
- Tests now properly validate against expected signatures

### 3. `test_signature.py` ✅
- Updated `generate_signature()` docstring with explanation
- Fixed commented example code to use `"application/json"`

### 4. `verify_signature.py` ✅
- Updated `generate_signature()` docstring with explanation
- Fixed signature generation call to use `"application/json"`

## Technical Details

### String to Sign Format
```
METHOD\n
CONTENT-MD5\n
application/json\n
TIME_IN_GMT\n
CANONICALIZED_RESOURCE
```

### HTTP Headers Sent
```
Content-Type: application/json;charset=UTF-8
Content-MD5: {base64_encoded_md5}
Time: {GMT_datetime_string}
Authorization: API {key_id}:{signature}
```

### Key Points
1. **Signature generation** uses `"application/json"` (no charset)
2. **HTTP header** sends `"application/json;charset=UTF-8"` (with charset)
3. **Time header** must be capitalized: `"Time"` not `"time"`
4. **Time format** must be GMT: `"Wed, 15 Oct 2025 00:00:29 GMT"`
5. **Authorization format**: `"API {key_id}:{signature}"`

## Validation

To test the fixes:
```bash
# Run the comprehensive test
python3 test_both_endpoints.py <key_id> <secret>

# Or run the verification script
python3 verify_signature.py <key_id> <secret>

# Or test the actual API integration
python3 test_api.py <key_id> <secret> <username>
```

## Expected Results
With these changes, the signature generation should now match the expected values:
- userStationList endpoint signature should be correct
- inverterDetail endpoint signature should be correct
- All API calls should succeed with proper authentication

## Reference
Based on the official Solis Cloud API TypeScript implementation provided by the user, which demonstrates the correct signature generation algorithm.
