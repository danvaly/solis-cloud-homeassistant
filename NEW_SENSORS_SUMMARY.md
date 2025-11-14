# New Sensors Added - October 15, 2025

## Summary
Added additional energy monitoring sensors for grid consumption, grid export, battery energy tracking, and home load consumption.

## New Sensors

### 1. Grid Consumption Sensors

#### Grid Purchased Today
- **Entity ID**: `sensor.{station_name}_grid_purchased_today`
- **API Field**: `gridPurchasedTodayEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Energy purchased from the grid today

#### Grid Purchased Total
- **Entity ID**: `sensor.{station_name}_grid_purchased_total`
- **API Field**: `gridPurchasedTotalEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Total energy purchased from the grid (lifetime)

### 2. Return to Grid Sensors (Grid Export)

#### Grid Sell Today
- **Entity ID**: `sensor.{station_name}_grid_sell_today`
- **API Field**: `gridSellTodayEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Energy exported to the grid today

#### Grid Sell Total
- **Entity ID**: `sensor.{station_name}_grid_sell_total`
- **API Field**: `gridSellTotalEnergyStr`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Total energy exported to the grid (lifetime)

### 3. Battery Energy Statistics

#### Battery Charge Today
- **Entity ID**: `sensor.{station_name}_battery_charge_today`
- **API Field**: `batteryTodayChargeEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Energy charged into the battery today

#### Battery Charge Total
- **Entity ID**: `sensor.{station_name}_battery_charge_total`
- **API Field**: `batteryTotalChargeEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Total energy charged into the battery (lifetime)

#### Battery Discharge Today
- **Entity ID**: `sensor.{station_name}_battery_discharge_today`
- **API Field**: `batteryTodayDischargeEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Energy discharged from the battery today

#### Battery Discharge Total
- **Entity ID**: `sensor.{station_name}_battery_discharge_total`
- **API Field**: `batteryTotalDischargeEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Total energy discharged from the battery (lifetime)

### 4. Home Load Energy Sensor

#### Home Load Today
- **Entity ID**: `sensor.{station_name}_home_load_today`
- **API Field**: `homeLoadTodayEnergy`
- **Unit**: kWh
- **Type**: Energy (Total Increasing)
- **Description**: Energy consumed by the house today

## Grid Carbon Footprint

### Note on Carbon Footprint Calculation
The Solis Cloud API does not provide direct carbon footprint data. However, you can calculate it in Home Assistant using:

1. **Template Sensor**: Create a template sensor that multiplies grid consumption by your local grid's carbon intensity factor
2. **Utility Meter**: Use Home Assistant's utility meter integration to track carbon footprint over time

### Example Template for Carbon Footprint:

```yaml
template:
  - sensor:
      - name: "Grid Carbon Footprint Today"
        unit_of_measurement: "kg CO2"
        state: >
          {% set grid_energy = states('sensor.your_station_grid_purchased_today') | float(0) %}
          {% set carbon_intensity = 0.233 %}  {# kg CO2 per kWh - adjust for your region #}
          {{ (grid_energy * carbon_intensity) | round(2) }}
        device_class: weight
```

### Carbon Intensity by Region (approximate values):
- **Europe Average**: ~0.233 kg CO2/kWh
- **Romania**: ~0.266 kg CO2/kWh
- **Germany**: ~0.310 kg CO2/kWh
- **France**: ~0.057 kg CO2/kWh (nuclear-heavy)
- **Poland**: ~0.750 kg CO2/kWh (coal-heavy)
- **UK**: ~0.233 kg CO2/kWh
- **USA Average**: ~0.386 kg CO2/kWh

Update the `carbon_intensity` value based on your specific region.

## Energy Dashboard Integration

All these sensors are compatible with Home Assistant's Energy Dashboard:

1. **Grid Consumption**: Use `Grid Purchased Today/Total` sensors
2. **Return to Grid**: Use `Grid Sell Today/Total` sensors
3. **Battery**: Use the charge/discharge sensors for battery monitoring

### How to Add to Energy Dashboard:

1. Go to **Settings** → **Dashboards** → **Energy**
2. **Grid Consumption**: Add `sensor.{station_name}_grid_purchased_total`
3. **Return to Grid**: Add `sensor.{station_name}_grid_sell_total`
4. **Battery Storage**:
   - **Energy going IN to the battery**: `sensor.{station_name}_battery_charge_total`
   - **Energy coming OUT of the battery**: `sensor.{station_name}_battery_discharge_total`
5. **Solar Production**: Use existing `sensor.{station_name}_energy_total`

## Utility Meter Integration

You can create daily, weekly, monthly, and yearly tracking using Home Assistant's Utility Meter integration:

```yaml
utility_meter:
  grid_purchased_daily:
    source: sensor.your_station_grid_purchased_total
    cycle: daily
  
  grid_purchased_monthly:
    source: sensor.your_station_grid_purchased_total
    cycle: monthly
  
  grid_sell_daily:
    source: sensor.your_station_grid_sell_total
    cycle: daily
  
  battery_charge_monthly:
    source: sensor.your_station_battery_charge_total
    cycle: monthly
  
  battery_discharge_monthly:
    source: sensor.your_station_battery_discharge_total
    cycle: monthly
```

## API Data Mapping

All sensor data comes from the `inverterDetail` endpoint:

| Sensor | API Field | Unit in API |
|--------|-----------|-------------|
| Grid Purchased Today | `gridPurchasedTodayEnergy` | kWh |
| Grid Purchased Total | `gridPurchasedTotalEnergy` | kWh |
| Grid Sell Today | `gridSellTodayEnergy` | kWh |
| Grid Sell Total | `gridSellTotalEnergy` | kWh |
| Battery Charge Today | `batteryTodayChargeEnergy` | kWh |
| Battery Charge Total | `batteryTotalChargeEnergy` | kWh |
| Battery Discharge Today | `batteryTodayDischargeEnergy` | kWh |
| Battery Discharge Total | `batteryTotalDischargeEnergy` | kWh |
| Home Load Today | `homeLoadTodayEnergy` | kWh |

## Testing

After restarting Home Assistant, you should see the new sensors appear automatically. Check:

```bash
# In Home Assistant Developer Tools → States
sensor.{your_station_name}_grid_purchased_today
sensor.{your_station_name}_grid_purchased_total
sensor.{your_station_name}_grid_sell_today
sensor.{your_station_name}_grid_sell_total
sensor.{your_station_name}_battery_charge_today
sensor.{your_station_name}_battery_charge_total
sensor.{your_station_name}_battery_discharge_today
sensor.{your_station_name}_battery_discharge_total
```

## Benefits

1. **Complete Energy Flow Visibility**: Track all energy movements (solar, grid, battery)
2. **Cost Tracking**: Calculate electricity costs based on grid consumption
3. **Battery Efficiency**: Monitor battery round-trip efficiency (discharge/charge ratio)
4. **Grid Independence**: Track how much you rely on the grid vs self-consumption
5. **Carbon Footprint**: Calculate environmental impact using template sensors

## Example Dashboard Card

```yaml
type: entities
title: Energy Statistics
entities:
  - entity: sensor.your_station_grid_purchased_today
    name: Grid Import Today
  - entity: sensor.your_station_grid_sell_today
    name: Grid Export Today
  - entity: sensor.your_station_battery_charge_today
    name: Battery Charged Today
  - entity: sensor.your_station_battery_discharge_today
    name: Battery Discharged Today
```
