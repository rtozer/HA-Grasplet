# Grasplet Home Assistant Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

A custom Home Assistant integration for monitoring Grasplet data-only SIM cards.

## Features

- **Real-time monitoring** of your Grasplet SIM cards
- **Secure credential storage** with masked password logging
- **Configurable polling interval** (1 hour to 1 week, default 24 hours)
- **Individual device per SIM** with comprehensive data tracking
- **Reconfigurable** credentials and settings

## Entities

For each SIM card, the integration creates the following entities:

| Entity | Description | Unit |
|--------|-------------|------|
| ICCID | SIM card identifier | - |
| Status | Current SIM status (ACTIVE, etc.) | - |
| Plan Name | Current data plan name | - |
| Expiry Date | Plan expiration date | timestamp |
| Data Limit | Total data allowance | GB |
| Data Remaining | Remaining data allowance (3 decimal precision) | GB |
| Availability Zone | Coverage area (e.g., "UK Only") | - |

## Installation

### HACS (Recommended)

#### Option 1: HACS Default Store (when approved)
1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Search for "Grasplet" and install

#### Option 2: Custom Repository
1. Open HACS in Home Assistant
2. Go to "Integrations" 
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/rtozer/HA-Grasplet`
6. Select "Integration" as the category
7. Click "Add"
8. Search for "Grasplet" and install

### Manual Installation

1. Copy the `custom_components/grasplet` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration through the UI

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "Grasplet"
3. Enter your credentials:
   - **Username**: Your Grasplet account email
   - **Password**: Your Grasplet account password  
   - **Poll Interval**: How often to check for updates (1-168 hours, default 24)

### Reconfiguration

You can update your credentials or poll interval at any time:

1. Go to **Settings** → **Devices & Services** 
2. Find the Grasplet integration
3. Click the three dots and select "Reconfigure"

## Security

- Passwords are securely stored using Home Assistant's credential storage
- Passwords are masked in all log output
- Authentication tokens are automatically managed and refreshed

## API Usage

The integration uses the official Grasplet API:
- Authentication: `https://data.grasplet.com/api/auth/login`
- Data retrieval: `https://data.grasplet.com/api/sim/all`

## Troubleshooting

### Authentication Issues
- Verify your Grasplet username (email) and password
- Check that your account is active and in good standing
- Try logging into the Grasplet web portal to confirm credentials

### Connection Issues  
- Ensure Home Assistant can reach `data.grasplet.com`
- Check your network firewall settings
- Verify internet connectivity from your Home Assistant instance

### Data Not Updating
- Check the poll interval setting - it may be set too long
- Look for error messages in Home Assistant logs
- Try reconfiguring the integration with fresh credentials

## Support

- [GitHub Issues](https://github.com/rtozer/HA-Grasplet/issues)
- [Home Assistant Community Forum](https://community.home-assistant.io/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial integration and is not affiliated with Grasplet. Use at your own risk.

[releases-shield]: https://img.shields.io/github/release/rtozer/HA-Grasplet.svg?style=for-the-badge
[releases]: https://github.com/rtozer/HA-Grasplet/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/rtozer/HA-Grasplet.svg?style=for-the-badge
[commits]: https://github.com/rtozer/HA-Grasplet/commits/main
[license-shield]: https://img.shields.io/github/license/rtozer/HA-Grasplet.svg?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge