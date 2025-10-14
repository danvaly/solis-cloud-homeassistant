"""Config flow for Solis Cloud integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .api import SolisCloudAPI

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("key_id"): str,
        vol.Required("secret"): str,
        vol.Required("username"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    api = SolisCloudAPI(
        key_id=data["key_id"],
        secret=data["secret"],
        username=data.get("username", ""),
    )

    try:
        result = await hass.async_add_executor_job(api.get_inverter_data)
        inverter_count = len(result.get("records", []))
        _LOGGER.info("Successfully validated connection, found %d inverter(s)", inverter_count)
    except Exception as err:
        _LOGGER.error("Error connecting to Solis Cloud: %s", err)
        raise CannotConnect from err

    # Use username if provided, otherwise use key_id
    title_name = data.get("username") or data["key_id"][:10]
    return {"title": f"Solis Cloud ({title_name})"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Solis Cloud."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
