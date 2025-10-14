# Solis Cloud Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release](https://img.shields.io/github/release/danvaly/solis-cloud-homeassistant.svg)](https://github.com/danvaly/solis-cloud-homeassistant/releases)
[![License](https://img.shields.io/github/license/danvaly/solis-cloud-homeassistant.svg)](LICENSE)

This integration allows you to monitor your Solis solar inverters through the Solis Cloud API in Home Assistant.

## Features

- Real-time monitoring of your Solis inverter
- Energy production tracking (today, month, year, total)
- Current power output
- Inverter status monitoring
- Automatic data updates every 5 minutes

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Add this repository as a custom repository in HACS:
   - Click on HACS in the sidebar
   - Click on "Integrations"
   - Click the three dots in the top right corner
   - Select "Custom repositories"
   - Add `https://github.com/danvaly/solis-cloud-homeassistant` as repository
   - Select "Integration" as category
3. Click "Install"
4. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/solis_cloud` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "+ Add Integration"
3. Search for "Solis Cloud"
4. Enter your Solis Cloud API credentials:
   - **API Key ID**: Your Solis Cloud API Key ID
   - **API Secret**: Your Solis Cloud API Secret
   - **Username**: Your Solis Cloud username

### Getting API Credentials

To obtain your API credentials:

1. Log in to [Solis Cloud](https://www.soliscloud.com)
2. Go to the API management section
3. Create a new API key
4. Copy the Key ID and Secret for use in this integration

## Sensors

The integration creates the following sensors for each inverter:

- **Current Power** - Current power output in watts
- **Energy Today** - Energy produced today in kWh
- **Energy This Month** - Energy produced this month in kWh
- **Energy This Year** - Energy produced this year in kWh
- **Energy Total** - Total energy produced in kWh
- **State** - Current inverter state (Online/Offline/Alarm)

## Support

If you encounter any issues or have suggestions, please [open an issue](https://github.com/danvaly/solis-cloud-homeassistant/issues) on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This integration is not officially associated with or endorsed by Solis or Ginlong Technologies.
