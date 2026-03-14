"""Solis Cloud API client."""
import hashlib
import hmac
import base64
import json
import logging
from datetime import datetime, timezone
from typing import Any

import requests

_LOGGER = logging.getLogger(__name__)


class SolisCloudAPI:
    """Solis Cloud API client."""

    def __init__(self, key_id: str, secret: str, username: str = "") -> None:
        """Initialize the API client."""
        self.key_id = key_id
        self.secret = secret
        self.username = username
        self.base_url = "https://www.soliscloud.com:13333"
        self._session = requests.Session()

    def _post(self, endpoint: str, payload: dict) -> dict[str, Any]:
        """Make an authenticated POST request to the Solis Cloud API."""
        url = f"{self.base_url}{endpoint}"
        body = json.dumps(payload, separators=(',', ':'))
        content_md5 = base64.b64encode(
            hashlib.md5(body.encode('utf-8')).digest()
        ).decode('utf-8')
        date_str = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

        # HMAC-SHA1 signature (content type without charset)
        string_to_sign = f"POST\n{content_md5}\napplication/json\n{date_str}\n{endpoint}"
        signature = base64.b64encode(
            hmac.new(
                self.secret.encode('utf-8'),
                msg=string_to_sign.encode('utf-8'),
                digestmod=hashlib.sha1,
            ).digest()
        ).decode('utf-8')

        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Content-MD5": content_md5,
            "Time": date_str,
            "Authorization": f"API {self.key_id}:{signature}",
        }

        _LOGGER.debug("POST %s", endpoint)
        response = self._session.post(url, data=body, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        if data.get("success") is not True:
            raise SolisAPIError(data.get("message", "Unknown error"))

        return data.get("data", {})

    def get_inverter_data(self) -> dict[str, Any]:
        """Get inverter data from Solis Cloud."""
        station_data = self._post("/v1/api/userStationList", {"pageNo": "1", "pageSize": "10"})
        stations = station_data.get("page", {}).get("records", [])

        if not stations:
            _LOGGER.warning("No stations found for this user")
            return {"records": []}

        all_inverters = []
        for station in stations:
            station_id = station.get("id")
            station_name = station.get("stationName", "Solis")

            inverters = self._get_station_inverters(station_id)
            for inv in inverters:
                inv["stationName"] = station_name
                inverter_id = inv.get("id")
                inverter_sn = inv.get("inverterSn")
                if inverter_id and inverter_sn:
                    details = self._get_inverter_detail(inverter_id, inverter_sn)
                    if details:
                        inv.update(details)
            all_inverters.extend(inverters)

        _LOGGER.debug("Retrieved %d inverter(s) with details", len(all_inverters))
        return {"records": all_inverters}

    def _get_station_inverters(self, station_id: str) -> list[dict[str, Any]]:
        """Get inverters for a specific station."""
        try:
            data = self._post("/v1/api/inverterList", {"stationId": str(station_id)})
            return data.get("page", {}).get("records", [])
        except Exception as e:
            _LOGGER.warning("Error getting inverters for station %s: %s", station_id, e)
            return []

    def _get_inverter_detail(self, inverter_id: str, inverter_sn: str) -> dict[str, Any]:
        """Get detailed inverter data."""
        try:
            return self._post("/v1/api/inverterDetail", {"id": str(inverter_id), "sn": str(inverter_sn)})
        except Exception as e:
            _LOGGER.warning("Error getting inverter detail for %s: %s", inverter_sn, e)
            return {}


class SolisAPIError(Exception):
    """Raised when the Solis Cloud API returns an error."""
