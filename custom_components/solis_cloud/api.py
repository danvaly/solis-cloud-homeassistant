"""Solis Cloud API client."""
import hashlib
import hmac
import base64
import json
import logging
from datetime import datetime
from typing import Any
import requests

_LOGGER = logging.getLogger(__name__)


class SolisCloudAPI:
    """Solis Cloud API client."""

    def __init__(self, key_id: str, secret: str, username: str = "") -> None:
        """Initialize the API client."""
        self.key_id = key_id
        self.secret = secret
        self.username = username  # Not used for userStationList endpoint
        self.base_url = "https://www.soliscloud.com:13333"

    def _get_content_md5(self, body: str) -> str:
        """Generate MD5 hash of the request body."""
        md5 = hashlib.md5()
        md5.update(body.encode('utf-8'))
        return base64.b64encode(md5.digest()).decode('utf-8')

    def _generate_signature(self, body: str, verb: str, content_md5: str, date: str, canonicalized_resource: str) -> str:
        """Generate HMAC-SHA1 signature for Solis Cloud API."""
        # Content type for signature should be "application/json" without charset
        content_type = "application/json"
        
        # Create the string to sign
        string_to_sign = f"{verb}\n{content_md5}\n{content_type}\n{date}\n{canonicalized_resource}"

        _LOGGER.debug("Signature generation:")
        _LOGGER.debug("  verb: %s", verb)
        _LOGGER.debug("  content_md5: %s", content_md5)
        _LOGGER.debug("  content_type: %s", content_type)
        _LOGGER.debug("  date: %s", date)
        _LOGGER.debug("  canonicalized_resource: %s", canonicalized_resource)
        _LOGGER.debug("  string_to_sign: %r", string_to_sign)

        # Generate HMAC-SHA1 signature
        hmac_obj = hmac.new(
            self.secret.encode('utf-8'),
            msg=string_to_sign.encode('utf-8'),
            digestmod=hashlib.sha1
        )
        signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')

        _LOGGER.debug("  signature: %s", signature)

        # Return Authorization header value
        authorization = f"API {self.key_id}:{signature}"
        _LOGGER.debug("  authorization: %s", authorization)
        return authorization

    def get_inverter_data(self) -> dict[str, Any]:
        """Get inverter data from Solis Cloud."""
        # First, get the list of stations (plants)
        url = f"{self.base_url}/v1/api/userStationList"

        # Prepare request body - get stations with pagination
        # Note: API expects string values, not integers
        body = json.dumps({"pageNo": "1", "pageSize": "10"}, separators=(',', ':'))
        content_type = "application/json;charset=UTF-8"

        # Generate Content-MD5
        content_md5 = self._get_content_md5(body)

        # Generate date in GMT format
        date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Generate authorization signature
        authorization = self._generate_signature(
            body=body,
            verb="POST",
            content_md5=content_md5,
            date=date_str,
            canonicalized_resource="/v1/api/userStationList"
        )

        # Prepare headers (note: use 'Time' instead of 'Date')
        headers = {
            "Content-Type": content_type,
            "Content-MD5": content_md5,
            "Time": date_str,
            "Authorization": authorization
        }

        _LOGGER.info("Making request to %s", url)
        _LOGGER.info("Request body: %s", body)
        _LOGGER.info("Request body (raw bytes): %r", body.encode('utf-8'))
        _LOGGER.info("Request headers:")
        for k, v in headers.items():
            _LOGGER.info("  %s: %s", k, v)

        try:
            # Get stations first
            response = requests.post(url, data=body, headers=headers, timeout=30)
            _LOGGER.debug("Response status code: %s", response.status_code)
            _LOGGER.debug("Response text: %s", response.text)

            response.raise_for_status()

            # Parse response
            data = response.json()
            _LOGGER.debug("Parsed JSON response: %s", data)

            if data.get("success") is True:
                station_data = data.get("data", {})
                stations = station_data.get("page", {}).get("records", [])

                if not stations:
                    _LOGGER.warning("No stations found for this user")
                    return {"records": []}

                # Get inverter details for each station
                all_inverters = []
                for station in stations:
                    station_id = station.get("id")
                    station_name = station.get("stationName", "Solis")
                    _LOGGER.debug("Getting inverters for station ID: %s", station_id)

                    inverters = self._get_station_inverters(station_id)
                    if inverters:
                        # Get detailed data for each inverter
                        for inv in inverters:
                            inv["stationName"] = station_name
                            # Fetch real-time inverter details
                            inverter_id = inv.get("id")
                            inverter_sn = inv.get("inverterSn")
                            if inverter_id and inverter_sn:
                                _LOGGER.debug("Fetching details for inverter %s", inverter_sn)
                                details = self.get_inverter_detail(inverter_id, inverter_sn)
                                if details:
                                    # Merge detail data into inverter record
                                    inv.update(details)
                        all_inverters.extend(inverters)

                result = {"records": all_inverters}
                _LOGGER.info("Successfully retrieved %d inverter(s) with details", len(all_inverters))
                return result
            else:
                error_msg = f"API error: {data.get('message', 'Unknown error')}"
                _LOGGER.error(error_msg)
                raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Request failed: %s", str(e))
            raise
        except Exception as e:
            _LOGGER.error("Unexpected error: %s", str(e))
            raise

    def _get_station_inverters(self, station_id: str) -> list[dict[str, Any]]:
        """Get inverters for a specific station."""
        url = f"{self.base_url}/v1/api/inverterList"

        # Prepare request body
        body = json.dumps({"stationId": str(station_id)}, separators=(',', ':'))
        content_type = "application/json;charset=UTF-8"

        # Generate Content-MD5
        content_md5 = self._get_content_md5(body)

        # Generate date in GMT format
        date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Generate authorization signature
        authorization = self._generate_signature(
            body=body,
            verb="POST",
            content_md5=content_md5,
            date=date_str,
            canonicalized_resource="/v1/api/inverterList"
        )

        # Prepare headers (note: use 'Time' instead of 'Date')
        headers = {
            "Content-Type": content_type,
            "Content-MD5": content_md5,
            "Time": date_str,
            "Authorization": authorization
        }

        try:
            response = requests.post(url, data=body, headers=headers, timeout=30)
            response.raise_for_status()

            data = response.json()
            _LOGGER.debug("Inverter list response: %s", data)

            if data.get("success") is True:
                inverter_data = data.get("data", {})
                return inverter_data.get("page", {}).get("records", [])
            else:
                _LOGGER.warning("Failed to get inverters for station %s: %s",
                              station_id, data.get("message", "Unknown error"))
                return []
        except Exception as e:
            _LOGGER.warning("Error getting inverters for station %s: %s", station_id, str(e))
            return []

    def get_inverter_detail(self, inverter_id: str, inverter_sn: str) -> dict[str, Any]:
        """Get detailed inverter data."""
        url = f"{self.base_url}/v1/api/inverterDetail"

        # Prepare request body - note the specific format
        body = json.dumps({
            "id": str(inverter_id),
            "sn": str(inverter_sn)
        }, separators=(',', ':'))
        content_type = "application/json;charset=UTF-8"

        # Generate Content-MD5
        content_md5 = self._get_content_md5(body)

        # Generate date in GMT format
        date_str = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

        # Generate authorization signature
        authorization = self._generate_signature(
            body=body,
            verb="POST",
            content_md5=content_md5,
            date=date_str,
            canonicalized_resource="/v1/api/inverterDetail"
        )

        # Prepare headers (note: use 'Time' instead of 'Date')
        headers = {
            "Content-Type": content_type,
            "Content-MD5": content_md5,
            "Time": date_str,
            "Authorization": authorization
        }

        _LOGGER.debug("Fetching inverter detail for ID=%s, SN=%s", inverter_id, inverter_sn)

        try:
            # Make request
            response = requests.post(url, data=body, headers=headers, timeout=30)
            response.raise_for_status()

            # Parse response
            data = response.json()
            _LOGGER.debug("Inverter detail response: %s", data)

            if data.get("success") is True:
                detail_data = data.get("data", {})
                _LOGGER.debug("Successfully retrieved inverter detail data with %d fields",
                            len(detail_data))
                return detail_data
            else:
                _LOGGER.warning("Failed to get inverter detail: %s",
                              data.get('message', 'Unknown error'))
                return {}
        except Exception as e:
            _LOGGER.warning("Error getting inverter detail for %s: %s", inverter_sn, str(e))
            return {}
