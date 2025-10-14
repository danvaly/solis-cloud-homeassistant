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

    def _generate_signature(self, body: str, verb: str = "POST", content_md5: str = "", content_type: str = "application/json", date: str = "", canonicalized_resource: str = "") -> str:
        """Generate HMAC-SHA1 signature for Solis Cloud API."""
        encrypt_str = verb + "\n" + content_md5 + "\n" + content_type + "\n" + date + "\n" + canonicalized_resource
        hmac_obj = hmac.new(
            self.secret.encode('utf-8'),
            msg=encrypt_str.encode('utf-8'),
            digestmod=hashlib.sha1
        )
        signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')
        return f"API {self.key_id}:{signature}"

    def get_inverter_data(self) -> dict[str, Any]:
        """Get inverter data from Solis Cloud."""
        url = f"{self.base_url}/v1/api/inverterList"

        body = json.dumps({"userid": self.username})
        content_type = "application/json"
        date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        headers = {
            "Content-Type": content_type,
            "Date": date_str,
            "Authorization": self._generate_signature(
                body=body,
                verb="POST",
                content_type=content_type,
                date=date_str,
                canonicalized_resource="/v1/api/inverterList"
            )
        }

        response = requests.post(url, data=body, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        if data.get("success") is True:
            return data.get("data", {})
        else:
            raise Exception(f"API error: {data.get('message', 'Unknown error')}")

    def get_inverter_detail(self, inverter_id: str, inverter_sn: str) -> dict[str, Any]:
        """Get detailed inverter data."""
        url = f"{self.base_url}/v1/api/inverterDetail"

        body = json.dumps({
            "id": inverter_id,
            "sn": inverter_sn
        })
        content_type = "application/json"
        date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        headers = {
            "Content-Type": content_type,
            "Date": date_str,
            "Authorization": self._generate_signature(
                body=body,
                verb="POST",
                content_type=content_type,
                date=date_str,
                canonicalized_resource="/v1/api/inverterDetail"
            )
        }

        response = requests.post(url, data=body, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        if data.get("success") is True:
            return data.get("data", {})
        else:
            raise Exception(f"API error: {data.get('message', 'Unknown error')}")
