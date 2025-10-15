"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    _LOGGER.info("Setting up Solis Cloud sensors")
    _LOGGER.debug("Coordinator data: %s", coordinator.data)

    entities = []

    if coordinator.data:
        # Check if data has "records" key (list of inverters)
        if "records" in coordinator.data:
            _LOGGER.info("Found %d inverters", len(coordinator.data["records"]))
            for inverter in coordinator.data["records"]:
                inverter_id = inverter.get("id")
                inverter_sn = inverter.get("inverterSn")
                station_name = inverter.get("stationName", "Solis")

                _LOGGER.info("Setting up inverter: %s (SN: %s)", station_name, inverter_sn)

                entities.extend([
                    # Current production in watts
                    SolisCloudSensor(
                        coordinator,
                        inverter_id,
                        inverter_sn,
                        station_name,
                        "pac",
                        "Current Production",
                        UnitOfPower.WATT,
                        SensorDeviceClass.POWER,
                        SensorStateClass.MEASUREMENT,
                    ),
                # Battery State of Charge (%)
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "batteryCapacitySoc",
                    "Battery SOC",
                    PERCENTAGE,
                    SensorDeviceClass.BATTERY,
                    SensorStateClass.MEASUREMENT,
                ),
                # Today production (kWh)
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "eToday",
                    "Today Production",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                # Grid consumption (W)
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "psum",
                    "Grid Consumption",
                    UnitOfPower.WATT,
                    SensorDeviceClass.POWER,
                    SensorStateClass.MEASUREMENT,
                ),
                # Battery state (charge/discharge)
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "batteryPower",
                    "Battery State",
                    UnitOfPower.WATT,
                    SensorDeviceClass.POWER,
                    SensorStateClass.MEASUREMENT,
                ),
                # Backup load (kWh)
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "familyLoadPower",
                    "Backup Load",
                    UnitOfPower.WATT,
                    SensorDeviceClass.POWER,
                    SensorStateClass.MEASUREMENT,
                ),
                # Current state
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "state",
                    "Current State",
                    None,
                    None,
                    None,
                ),
                # Inverter temperature
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "inverterTemperature",
                    "Inverter Temperature",
                    UnitOfTemperature.CELSIUS,
                    SensorDeviceClass.TEMPERATURE,
                    SensorStateClass.MEASUREMENT,
                ),
                # Additional useful sensors
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "eMonth",
                    "Energy This Month",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL,
                ),
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "eYear",
                    "Energy This Year",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL,
                ),
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "eTotal",
                    "Energy Total",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                # Grid consumption sensors
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "gridPurchasedTodayEnergy",
                    "Grid Purchased Today",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "gridPurchasedTotalEnergy",
                    "Grid Purchased Total",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                # Return to grid sensors
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "gridSellTodayEnergy",
                    "Grid Sell Today",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "gridSellTotalEnergy",
                    "Grid Sell Total",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                # Battery charge energy sensors
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "batteryTodayChargeEnergy",
                    "Battery Charge Today",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "batteryTotalChargeEnergy",
                    "Battery Charge Total",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                # Battery discharge energy sensors
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "batteryTodayDischargeEnergy",
                    "Battery Discharge Today",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "batteryTotalDischargeEnergy",
                    "Battery Discharge Total",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
                ])
        else:
            _LOGGER.warning("No 'records' key in coordinator data. Data structure: %s", list(coordinator.data.keys()) if isinstance(coordinator.data, dict) else type(coordinator.data))
    else:
        _LOGGER.warning("No data available from coordinator")

    _LOGGER.info("Created %d sensor entities", len(entities))
    async_add_entities(entities)


class SolisCloudSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Solis Cloud Sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        inverter_id: str,
        inverter_sn: str,
        station_name: str,
        sensor_key: str,
        sensor_name: str,
        unit: str | None,
        device_class: SensorDeviceClass | None,
        state_class: SensorStateClass | None,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._inverter_id = inverter_id
        self._inverter_sn = inverter_sn
        self._sensor_key = sensor_key
        self._attr_name = f"{station_name} {sensor_name}"
        self._attr_unique_id = f"{inverter_sn}_{sensor_key}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._inverter_sn)},
            "name": f"Solis Inverter {self._inverter_sn}",
            "manufacturer": "Solis",
            "model": "Solar Inverter",
        }

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data and "records" in self.coordinator.data:
            for inverter in self.coordinator.data["records"]:
                if inverter.get("id") == self._inverter_id:
                    value = inverter.get(self._sensor_key)

                    # Convert state code to readable text
                    if self._sensor_key == "state":
                        state_map = {
                            "1": "Online",
                            "2": "Offline",
                            "3": "Alarm",
                        }
                        return state_map.get(str(value), "Unknown")

                    return value
        return None

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        if self._sensor_key == "batteryPower":
            # Add battery state as attribute
            if self.coordinator.data and "records" in self.coordinator.data:
                for inverter in self.coordinator.data["records"]:
                    if inverter.get("id") == self._inverter_id:
                        power = inverter.get("batteryPower", 0)
                        if power > 0:
                            state = "Charging"
                        elif power < 0:
                            state = "Discharging"
                        else:
                            state = "Idle"
                        return {
                            "battery_state": state,
                            "power": abs(power) if power else 0
                        }
        return None
