# Quick Installation Guide for New Sensors

## What Was Added

✅ **8 new energy sensors** have been added to track:
- Grid consumption (import from grid)
- Grid export (return to grid) 
- Battery charge energy (energy going INTO battery)
- Battery discharge energy (energy coming OUT of battery)

All sensors measure energy in **kWh** and are fully compatible with Home Assistant's Energy Dashboard.

## Installation Steps

### 1. Update the Integration

If you're using HACS:
```bash
# Update through HACS UI
# Go to HACS → Integrations → Solis Cloud → Update
```

If you're installing manually:
```bash
# Copy the updated files to your custom_components folder
cp -r custom_components/solis_cloud /config/custom_components/
```

### 2. Restart Home Assistant

```bash
# From Home Assistant UI:
# Settings → System → Restart

# Or via CLI:
ha core restart
```

### 3. Verify Sensors

After restart, check Developer Tools → States for new sensors:
- `sensor.{station}_grid_purchased_today`
- `sensor.{station}_grid_purchased_total`
- `sensor.{station}_grid_sell_today`
- `sensor.{station}_grid_sell_total`
- `sensor.{station}_battery_charge_today`
- `sensor.{station}_battery_charge_total`
- `sensor.{station}_battery_discharge_today`
- `sensor.{station}_battery_discharge_total`

Replace `{station}` with your actual station name (e.g., "Ghica Valentin Danut CV24").

## Quick Setup: Energy Dashboard

### Add to Energy Dashboard (Recommended!)

1. Go to **Settings** → **Dashboards** → **Energy**

2. **Grid Consumption Section**:
   - Click "Add Consumption"
   - Select: `sensor.{station}_grid_purchased_total`
   - Set entity type: "Grid consumption"

3. **Return to Grid Section**:
   - Click "Add Return" 
   - Select: `sensor.{station}_grid_sell_total`

4. **Battery Storage Section**:
   - Click "Add Battery System"
   - **Energy going IN**: `sensor.{station}_battery_charge_total`
   - **Energy coming OUT**: `sensor.{station}_battery_discharge_total`

5. **Solar Panels** (if not already added):
   - Select: `sensor.{station}_energy_total`

6. Click **Save**

The Energy Dashboard will now show complete energy flow!

## Sample Dashboard Card

Add this to your Lovelace dashboard:

```yaml
type: vertical-stack
cards:
  - type: entity
    entity: sensor.your_station_grid_purchased_today
    name: Grid Import Today
    icon: mdi:transmission-tower-import
  
  - type: entity
    entity: sensor.your_station_grid_sell_today
    name: Grid Export Today
    icon: mdi:transmission-tower-export
  
  - type: entity
    entity: sensor.your_station_battery_charge_today
    name: Battery Charged Today
    icon: mdi:battery-charging-50
  
  - type: entity
    entity: sensor.your_station_battery_discharge_today
    name: Battery Used Today
    icon: mdi:battery-minus
```

## Calculate Carbon Footprint (Optional)

Add this to your `configuration.yaml`:

```yaml
template:
  - sensor:
      - name: "Grid Carbon Footprint Today"
        unique_id: grid_carbon_footprint_today
        unit_of_measurement: "kg CO2"
        state: >
          {% set grid_energy = states('sensor.your_station_grid_purchased_today') | float(0) %}
          {% set carbon_intensity = 0.266 %}  {# Romania average #}
          {{ (grid_energy * carbon_intensity) | round(2) }}
        device_class: weight
      
      - name: "Grid Carbon Footprint Total"
        unique_id: grid_carbon_footprint_total
        unit_of_measurement: "kg CO2"
        state: >
          {% set grid_energy = states('sensor.your_station_grid_purchased_total') | float(0) %}
          {% set carbon_intensity = 0.266 %}  {# Romania average #}
          {{ (grid_energy * carbon_intensity) | round(2) }}
        device_class: weight
```

**Adjust carbon intensity for your region:**
- Romania: 0.266 kg CO2/kWh
- EU Average: 0.233 kg CO2/kWh
- Check [Electricity Map](https://app.electricitymaps.com/) for your specific region

## Automation Examples

### Alert When Grid Import is High

```yaml
automation:
  - alias: "High Grid Import Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.your_station_grid_purchased_today
        above: 10  # Alert if more than 10 kWh imported today
    action:
      - service: notify.mobile_app
        data:
          title: "High Grid Import"
          message: "Grid import today: {{ states('sensor.your_station_grid_purchased_today') }} kWh"
```

### Track Battery Efficiency

```yaml
template:
  - sensor:
      - name: "Battery Efficiency Today"
        unique_id: battery_efficiency_today
        unit_of_measurement: "%"
        state: >
          {% set charge = states('sensor.your_station_battery_charge_today') | float(0) %}
          {% set discharge = states('sensor.your_station_battery_discharge_today') | float(0) %}
          {% if charge > 0 %}
            {{ ((discharge / charge) * 100) | round(1) }}
          {% else %}
            0
          {% endif %}
```

## Troubleshooting

### Sensors Show "Unknown" or "Unavailable"

1. Check if the integration is working:
   ```
   Settings → Devices & Services → Solis Cloud
   ```

2. Check logs for errors:
   ```
   Settings → System → Logs
   Filter: "solis_cloud"
   ```

3. Verify API credentials are correct

4. Try reloading the integration:
   ```
   Settings → Devices & Services → Solis Cloud → ⋮ → Reload
   ```

### Sensors Not Appearing

1. Make sure you restarted Home Assistant after updating
2. Check that the sensor keys match your API data
3. Review logs for any errors during sensor setup

### Energy Dashboard Not Updating

1. Energy dashboard updates every hour by default
2. Force update by reloading the integration
3. Check that sensors have `state_class: total_increasing`

## API Data Fields

These sensors pull data from the Solis Cloud `inverterDetail` endpoint:

```json
{
  "gridPurchasedTodayEnergy": 0.820,
  "gridPurchasedTotalEnergy": 123.230,
  "gridSellTodayEnergy": 0.000,
  "gridSellTotalEnergy": 2.930,
  "batteryTodayChargeEnergy": 0.000,
  "batteryTotalChargeEnergy": 174.000,
  "batteryTodayDischargeEnergy": 0.000,
  "batteryTotalDischargeEnergy": 195.000
}
```

All values are in kWh as provided by the API.

## Need Help?

Check the project documentation:
- [README.md](./README.md) - Main documentation
- [NEW_SENSORS_SUMMARY.md](./NEW_SENSORS_SUMMARY.md) - Detailed sensor information
- [SIGNATURE_FIX_SUMMARY.md](./SIGNATURE_FIX_SUMMARY.md) - API authentication details

## Summary

You now have complete visibility into:
- ⚡ Grid consumption and export
- 🔋 Battery charge and discharge energy
- 🌍 Carbon footprint calculation (optional)
- 📊 Full Energy Dashboard integration

Enjoy your enhanced energy monitoring! 🎉
