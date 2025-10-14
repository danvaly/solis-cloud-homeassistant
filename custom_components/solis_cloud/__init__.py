"""The Solis Cloud integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .api import SolisCloudAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Solis Cloud from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    _LOGGER.info("Setting up Solis Cloud integration")
    _LOGGER.debug("Config entry data: key_id=%s, username=%s",
                  entry.data.get("key_id"), entry.data.get("username"))

    api = SolisCloudAPI(
        key_id=entry.data["key_id"],
        secret=entry.data["secret"],
        username=entry.data["username"],
    )

    async def async_update_data():
        """Fetch data from API."""
        _LOGGER.debug("Starting data fetch from Solis Cloud API")
        try:
            data = await hass.async_add_executor_job(api.get_inverter_data)
            _LOGGER.info("Successfully received data from Solis Cloud API")
            _LOGGER.debug("Data structure: %s", data)
            return data
        except Exception as err:
            _LOGGER.error("Error communicating with API: %s", err, exc_info=True)
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
        update_method=async_update_data,
        update_interval=timedelta(minutes=5),
    )

    _LOGGER.info("Performing initial data refresh")
    try:
        await coordinator.async_config_entry_first_refresh()
        _LOGGER.info("Initial data refresh completed successfully")
    except Exception as err:
        _LOGGER.error("Initial data refresh failed: %s", err, exc_info=True)
        raise

    hass.data[DOMAIN][entry.entry_id] = coordinator

    _LOGGER.info("Setting up sensor platform")
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    _LOGGER.info("Solis Cloud integration setup completed")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
