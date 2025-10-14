"""Solis Cloud API client."""
import hashlib
import hmac
import base64
import json
from datetime import datetime
from typing import Any
import requests


class SolisCloudAPI:
    """Solis Cloud API client."""

    def __init__(self, key_id: str, secret: str, username: str) -> None:
        """Initialize the API client."""
        self.key_id = key_id
        self.secret = secret
        self.username = username
        self.base_url = "https://www.soliscloud.com:13333"

    def _get_content_md5(self, body: str) -> str:
        """Generate MD5 hash of the request body."""
        md5 = hashlib.md5()
        md5.update(body.encode('utf-8'))
        return base64.b64encode(md5.digest()).decode('utf-8')

    def _generate_signature(self, body: str, verb: str, content_md5: str, content_type: str, date: str, canonicalized_resource: str) -> str:
        """Generate HMAC-SHA1 signature for Solis Cloud API."""
        # Create the string to sign
        string_to_sign = f"{verb}\n{content_md5}\n{content_type}\n{date}\n{canonicalized_resource}"

        # Generate HMAC-SHA1 signature
        hmac_obj = hmac.new(
            self.secret.encode('utf-8'),
            msg=string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha1
        )
        signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')

        # Return Authorization header value
        return f"API {self.key_id}:{signature}"

    def get_inverter_data(self) -> dict[str, Any]:
        """Get inverter data from Solis Cloud."""
        url = f"{self.base_url}/v1/api/inverterList"

        # Prepare request body
        body = json.dumps({"userid": self.username})
        content_type = "application/json"

        # Generate Content-MD5
        content_md5 = self._get_content_md5(body)

        # Generate date in GMT format
        date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Generate authorization signature
        authorization = self._generate_signature(
            body=body,
            verb="POST",
            content_md5=content_md5,
            content_type=content_type,
            date=date_str,
            canonicalized_resource="/v1/api/inverterList"
        )

        # Prepare headers
        headers = {
            "Content-Type": content_type,
            "Content-MD5": content_md5,
            "Date": date_str,
            "Authorization": authorization
        }

        # Make request
        response = requests.post(url, data=body, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse response
        data = response.json()
        if data.get("success") is True:
            return data.get("data", {})
        else:
            raise Exception(f"API error: {data.get('message', 'Unknown error')}")

    def get_inverter_detail(self, inverter_id: str, inverter_sn: str) -> dict[str, Any]:
        """Get detailed inverter data."""
        url = f"{self.base_url}/v1/api/inverterDetail"

        # Prepare request body
        body = json.dumps({
            "id": inverter_id,
            "sn": inverter_sn
        })
        content_type = "application/json"

        # Generate Content-MD5
        content_md5 = self._get_content_md5(body)

        # Generate date in GMT format
        date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Generate authorization signature
        authorization = self._generate_signature(
            body=body,
            verb="POST",
            content_md5=content_md5,
            content_type=content_type,
            date=date_str,
            canonicalized_resource="/v1/api/inverterDetail"
        )

        # Prepare headers
        headers = {
            "Content-Type": content_type,
            "Content-MD5": content_md5,
            "Date": date_str,
            "Authorization": authorization
        }

        # Make request
        response = requests.post(url, data=body, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse response
        data = response.json()
        if data.get("success") is True:
            return data.get("data", {})
        else:
            raise Exception(f"API error: {data.get('message', 'Unknown error')}")
