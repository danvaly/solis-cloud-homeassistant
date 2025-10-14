"""Platform for sensor integration."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []

    if coordinator.data and "records" in coordinator.data:
        for inverter in coordinator.data["records"]:
            inverter_id = inverter.get("id")
            inverter_sn = inverter.get("inverterSn")
            station_name = inverter.get("stationName", "Solis")

            entities.extend([
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "pac",
                    "Current Power",
                    UnitOfPower.WATT,
                    SensorDeviceClass.POWER,
                    SensorStateClass.MEASUREMENT,
                ),
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "eToday",
                    "Energy Today",
                    UnitOfEnergy.KILO_WATT_HOUR,
                    SensorDeviceClass.ENERGY,
                    SensorStateClass.TOTAL_INCREASING,
                ),
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
                SolisCloudSensor(
                    coordinator,
                    inverter_id,
                    inverter_sn,
                    station_name,
                    "state",
                    "State",
                    None,
                    None,
                    None,
                ),
            ])

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
