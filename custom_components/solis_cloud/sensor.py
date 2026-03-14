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
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
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

# Sensor definitions: (api_key, name, unit, device_class, state_class)
SENSOR_DEFINITIONS = [
    # --- Power ---
    ("pac", "Current Production", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
    ("psum", "Grid Power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
    ("familyLoadPower", "Backup Load", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
    ("totalLoadPower", "House Power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),
    ("batteryPower", "Battery Power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),

    # --- Solar Production Energy ---
    ("eToday", "Production Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("eMonth", "Production This Month", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL),
    ("eYear", "Production This Year", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL),
    ("eTotal", "Production Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),

    # --- Grid Energy ---
    ("gridPurchasedTodayEnergy", "Grid Import Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("gridPurchasedTotalEnergy", "Grid Import Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("gridSellTodayEnergy", "Grid Export Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("gridSellTotalEnergy", "Grid Export Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),

    # --- Battery Energy ---
    ("batteryCapacitySoc", "Battery SOC", PERCENTAGE, SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT),
    ("batteryTodayChargeEnergy", "Battery Charge Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("batteryTotalChargeEnergy", "Battery Charge Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("batteryTodayDischargeEnergy", "Battery Discharge Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("batteryTotalDischargeEnergy", "Battery Discharge Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("batteryVoltage", "Battery Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("batteryCurrent", "Battery Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("soh", "Battery SOH", PERCENTAGE, SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT),
    ("batteryHealthState", "Battery Health State", None, None, None),

    # --- Home Load Energy ---
    ("homeLoadTodayEnergy", "Home Load Today", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),
    ("homeLoadTotalEnergy", "Home Load Total", UnitOfEnergy.KILO_WATT_HOUR, SensorDeviceClass.ENERGY, SensorStateClass.TOTAL_INCREASING),

    # --- PV String 1 ---
    ("uPv1", "PV1 Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("iPv1", "PV1 Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("pow1", "PV1 Power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),

    # --- PV String 2 ---
    ("uPv2", "PV2 Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("iPv2", "PV2 Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("pow2", "PV2 Power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),

    # --- PV String 3 ---
    ("uPv3", "PV3 Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("iPv3", "PV3 Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("pow3", "PV3 Power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),

    # --- PV String 4 ---
    ("uPv4", "PV4 Voltage", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("iPv4", "PV4 Current", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("pow4", "PV4 Power", UnitOfPower.WATT, SensorDeviceClass.POWER, SensorStateClass.MEASUREMENT),

    # --- AC Output ---
    ("uAc1", "AC Voltage L1", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("iAc1", "AC Current L1", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("uAc2", "AC Voltage L2", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("iAc2", "AC Current L2", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("uAc3", "AC Voltage L3", UnitOfElectricPotential.VOLT, SensorDeviceClass.VOLTAGE, SensorStateClass.MEASUREMENT),
    ("iAc3", "AC Current L3", UnitOfElectricCurrent.AMPERE, SensorDeviceClass.CURRENT, SensorStateClass.MEASUREMENT),
    ("fac", "Grid Frequency", UnitOfFrequency.HERTZ, SensorDeviceClass.FREQUENCY, SensorStateClass.MEASUREMENT),

    # --- Status ---
    ("state", "Current State", None, None, None),
    ("inverterTemperature", "Inverter Temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT),
    ("currentState", "Operating State", None, None, None),
]


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
        if "records" in coordinator.data:
            _LOGGER.info("Found %d inverters", len(coordinator.data["records"]))
            for inverter in coordinator.data["records"]:
                inverter_id = inverter.get("id")
                inverter_sn = inverter.get("inverterSn")
                station_name = inverter.get("stationName", "Solis")

                _LOGGER.info("Setting up inverter: %s (SN: %s)", station_name, inverter_sn)

                for api_key, name, unit, device_class, state_class in SENSOR_DEFINITIONS:
                    # Only create sensor if the API returned this field
                    if api_key in inverter:
                        entities.append(
                            SolisCloudSensor(
                                coordinator,
                                inverter_id,
                                inverter_sn,
                                station_name,
                                api_key,
                                name,
                                unit,
                                device_class,
                                state_class,
                            )
                        )
                    else:
                        _LOGGER.debug("Skipping sensor '%s' - key '%s' not in API data", name, api_key)
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

    def _get_inverter_data(self) -> dict | None:
        """Find this sensor's inverter data from the coordinator."""
        if self.coordinator.data and "records" in self.coordinator.data:
            for inverter in self.coordinator.data["records"]:
                if inverter.get("id") == self._inverter_id:
                    return inverter
        return None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        inverter = self._get_inverter_data()
        if inverter is None:
            return None

        value = inverter.get(self._sensor_key)

        if self._sensor_key == "state":
            state_map = {"1": "Online", "2": "Offline", "3": "Alarm"}
            return state_map.get(str(value), "Unknown")

        return value

    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        if self._sensor_key != "batteryPower":
            return None

        inverter = self._get_inverter_data()
        if inverter is None:
            return None

        power = inverter.get("batteryPower", 0)
        if power > 0:
            state = "Charging"
        elif power < 0:
            state = "Discharging"
        else:
            state = "Idle"
        return {"battery_state": state, "power": abs(power) if power else 0}
