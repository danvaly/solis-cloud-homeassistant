#!/usr/bin/env python3
"""Test script for Solis Cloud API."""
import sys
import json
from custom_components.solis_cloud.api import SolisCloudAPI

def main():
    """Test the Solis Cloud API connection."""
    if len(sys.argv) < 4:
        print("Usage: python3 test_api.py <key_id> <secret> <username>")
        sys.exit(1)

    key_id = sys.argv[1]
    secret = sys.argv[2]
    username = sys.argv[3]

    print("=" * 60)
    print("Testing Solis Cloud API Connection")
    print("=" * 60)
    print(f"Key ID: {key_id}")
    print(f"Username: {username}")
    print()

    api = SolisCloudAPI(key_id=key_id, secret=secret, username=username)

    try:
        print("Fetching inverter data...")
        data = api.get_inverter_data()

        print("\n" + "=" * 60)
        print("SUCCESS! API Response:")
        print("=" * 60)
        print(json.dumps(data, indent=2))
        print()

        # Analyze the data structure
        print("=" * 60)
        print("Data Structure Analysis:")
        print("=" * 60)

        if isinstance(data, dict):
            print(f"Type: Dictionary")
            print(f"Keys: {list(data.keys())}")
            print()

            if "records" in data:
                records = data["records"]
                print(f"Found {len(records)} inverter(s)")
                print()

                for i, inverter in enumerate(records, 1):
                    print(f"Inverter {i}:")
                    print(f"  ID: {inverter.get('id')}")
                    print(f"  Serial Number: {inverter.get('inverterSn')}")
                    print(f"  Station Name: {inverter.get('stationName')}")
                    print(f"  All available fields: {list(inverter.keys())}")
                    print()
            else:
                print("WARNING: No 'records' key found in data!")
                print("This may cause issues with sensor setup.")
        else:
            print(f"WARNING: Expected dict, got {type(data)}")

    except Exception as e:
        print("\n" + "=" * 60)
        print("ERROR!")
        print("=" * 60)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
