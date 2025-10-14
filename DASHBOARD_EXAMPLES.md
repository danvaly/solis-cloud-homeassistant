# Dashboard Examples

This document provides detailed examples and visual descriptions of dashboard configurations for the Solis Cloud integration.

## Example 1: Complete Solar Dashboard

A comprehensive dashboard showing all aspects of your solar system:

```yaml
title: Solar System
type: vertical-stack
cards:
  # Main Status Card
  - type: entities
    title: Solis Solar System
    show_header_toggle: false
    state_color: true
    entities:
      - entity: sensor.solis_current_state
        name: System Status
        icon: mdi:solar-power
      - type: divider
      - entity: sensor.solis_current_production
        name: Current Production
        icon: mdi:solar-power-variant
      - entity: sensor.solis_battery_soc
        name: Battery Level
        icon: mdi:battery-high
      - entity: sensor.solis_grid_consumption
        name: Grid Power
        icon: mdi:transmission-tower
      - entity: sensor.solis_backup_load
        name: House Load
        icon: mdi:home-lightning-bolt
      - type: divider
      - entity: sensor.solis_inverter_temperature
        name: Inverter Temp
        icon: mdi:thermometer

  # Power Gauges
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.solis_current_production
        name: Solar
        min: 0
        max: 6000
        segments:
          - from: 0
            color: '#db4437'
          - from: 1000
            color: '#ffa600'
          - from: 3000
            color: '#43a047'
      - type: gauge
        entity: sensor.solis_battery_soc
        name: Battery
        min: 0
        max: 100
        segments:
          - from: 0
            color: '#db4437'
          - from: 20
            color: '#ffa600'
          - from: 50
            color: '#43a047'

  # Production Statistics
  - type: entities
    title: Energy Production
    entities:
      - entity: sensor.solis_today_production
        name: Today
        icon: mdi:calendar-today
      - entity: sensor.solis_energy_this_month
        name: This Month
        icon: mdi:calendar-month
      - entity: sensor.solis_energy_this_year
        name: This Year
        icon: mdi:calendar-range
      - entity: sensor.solis_energy_total
        name: Lifetime Total
        icon: mdi:counter

  # 24-Hour History
  - type: history-graph
    title: Power Production (24h)
    hours_to_show: 24
    entities:
      - entity: sensor.solis_current_production
        name: Solar Power
```

## Example 2: Minimal Card (Mobile Optimized)

Perfect for quick glances on mobile devices:

```yaml
type: glance
title: Solar
show_name: true
show_state: true
columns: 4
entities:
  - entity: sensor.solis_current_production
    name: Power
    icon: mdi:solar-power
  - entity: sensor.solis_battery_soc
    name: Battery
    icon: mdi:battery
  - entity: sensor.solis_today_production
    name: Today
    icon: mdi:flash
  - entity: sensor.solis_current_state
    name: Status
    icon: mdi:information
```

## Example 3: Energy Flow Visualization

Visual representation of energy flowing through your system:

```yaml
type: vertical-stack
cards:
  # Simple Flow Description
  - type: markdown
    content: |
      ## Solar Energy Flow

      **Solar** → **Battery/House** → **Grid**

      Current Status: {{ states('sensor.solis_current_state') }}

  # Power Values
  - type: horizontal-stack
    cards:
      - type: entity
        entity: sensor.solis_current_production
        name: Solar
        icon: mdi:white-balance-sunny
      - type: entity
        entity: sensor.solis_battery_state
        name: Battery
        icon: mdi:battery-charging
      - type: entity
        entity: sensor.solis_backup_load
        name: House
        icon: mdi:home

  # Battery Status
  - type: entity
    entity: sensor.solis_battery_soc
    name: Battery Level
    icon: mdi:battery-80
    attribute: battery_state
```

## Example 4: Statistics Card

Show energy statistics with visual bars:

```yaml
type: statistics-graph
title: Solar Energy Statistics
entities:
  - sensor.solis_current_production
stat_types:
  - mean
  - min
  - max
period:
  calendar:
    period: day
chart_type: bar
```

## Example 5: Grid Card with Battery Details

Focus on battery and grid interaction:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: Battery & Grid
    entities:
      - type: custom:bar-card
        entity: sensor.solis_battery_soc
        name: Battery Charge
        max: 100
        positions:
          icon: inside
          indicator: inside
          name: inside
        severity:
          - from: 0
            to: 20
            color: '#db4437'
          - from: 21
            to: 50
            color: '#ffa600'
          - from: 51
            to: 100
            color: '#43a047'
      - entity: sensor.solis_battery_state
        secondary_info: last-changed
      - type: divider
      - entity: sensor.solis_grid_consumption
        name: Grid Power
      - entity: sensor.solis_backup_load
        name: House Consumption
```

## Example 6: Conditional Card (Show Warnings)

Display warnings when temperature is high or battery is low:

```yaml
type: conditional
conditions:
  - entity: sensor.solis_inverter_temperature
    state_not: unavailable
card:
  type: markdown
  content: |
    {% if states('sensor.solis_inverter_temperature')|float > 60 %}
    ⚠️ **Warning**: Inverter temperature is high ({{ states('sensor.solis_inverter_temperature') }}°C)
    {% endif %}

    {% if states('sensor.solis_battery_soc')|float < 20 %}
    🔋 **Low Battery**: Battery at {{ states('sensor.solis_battery_soc') }}%
    {% endif %}

    {% if is_state('sensor.solis_current_state', 'Alarm') %}
    🚨 **ALARM**: System requires attention!
    {% endif %}
```

## Example 7: Energy Dashboard Integration

Add to Home Assistant's built-in Energy Dashboard:

1. Go to **Settings** → **Dashboards** → **Energy**
2. Configure as follows:

### Solar Panels
- Add: `sensor.solis_today_production`

### Battery Systems
- Add: `sensor.solis_battery_state`
- State of charge: `sensor.solis_battery_soc`

### Grid Consumption
- Add: `sensor.solis_grid_consumption` (if available as cumulative kWh)

### Home Battery Storage
- Energy going in: Battery charging
- Energy going out: Battery discharging

## Example 8: Full-Width Dashboard

Complete solar monitoring page:

```yaml
title: Solar Monitoring
path: solar
icon: mdi:solar-power
badges: []
cards:
  - type: vertical-stack
    cards:
      # Header
      - type: markdown
        content: |
          # ☀️ Solar Energy System
          Last updated: {{ as_timestamp(now()) | timestamp_custom('%H:%M:%S') }}

      # Main Status
      - type: horizontal-stack
        cards:
          - type: entity
            entity: sensor.solis_current_state
            name: Status
            icon: mdi:information-outline
          - type: entity
            entity: sensor.solis_current_production
            name: Production
            icon: mdi:solar-power
          - type: entity
            entity: sensor.solis_battery_soc
            name: Battery
            icon: mdi:battery
          - type: entity
            entity: sensor.solis_inverter_temperature
            name: Temperature
            icon: mdi:thermometer

      # Power Flow
      - type: entities
        title: Power Flow
        entities:
          - entity: sensor.solis_current_production
            name: Solar Production
            icon: mdi:solar-panel
          - entity: sensor.solis_backup_load
            name: House Load
            icon: mdi:home-import-outline
          - entity: sensor.solis_grid_consumption
            name: Grid Import/Export
            icon: mdi:transmission-tower
          - entity: sensor.solis_battery_state
            name: Battery Power
            icon: mdi:battery-arrow-up

      # Production Stats
      - type: horizontal-stack
        cards:
          - type: statistic
            entity: sensor.solis_today_production
            name: Today
            period:
              calendar:
                period: day
          - type: statistic
            entity: sensor.solis_energy_this_month
            name: This Month
            period:
              calendar:
                period: month
          - type: statistic
            entity: sensor.solis_energy_this_year
            name: This Year
            period:
              calendar:
                period: year

      # History
      - type: history-graph
        title: 24-Hour Production
        hours_to_show: 24
        entities:
          - entity: sensor.solis_current_production
            name: Power
```

## Recommended HACS Frontend Cards

For enhanced visualizations, install these from HACS → Frontend:

1. **ApexCharts Card** - Advanced, customizable charts
2. **Mini Graph Card** - Compact line graphs
3. **Bar Card** - Horizontal/vertical bar displays
4. **Button Card** - Highly customizable buttons
5. **Mushroom Cards** - Modern, clean card designs
6. **Power Flow Card Plus** - Animated power flow
7. **Auto Entities** - Dynamic card generation
8. **Card Mod** - Style any card with CSS

## Tips

- **Entity Names**: Replace `solis` with your actual inverter serial number
- **Max Values**: Adjust gauge max values based on your system capacity
- **Colors**: Customize severity ranges to match your preferences
- **Icons**: Browse [Material Design Icons](https://materialdesignicons.com/) for alternatives
- **Refresh Rate**: Data updates every 5 minutes automatically
- **Mobile**: Test your cards on mobile devices for optimal layout

## Color Scheme

Recommended colors for solar monitoring:

- **Solar Production**: `#FFA500` (Orange) or `#FFD700` (Gold)
- **Battery Charging**: `#43A047` (Green)
- **Battery Discharging**: `#FB8C00` (Deep Orange)
- **Grid Import**: `#E53935` (Red)
- **Grid Export**: `#43A047` (Green)
- **House Load**: `#1E88E5` (Blue)
