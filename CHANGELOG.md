# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).



## [1.0.0] - 2025-01-01

### Added
- Initial release of Grasplet Home Assistant integration
- Support for monitoring multiple Grasplet data-only SIM cards
- Secure credential storage with masked password logging
- Configurable polling interval (1-168 hours, default 24 hours)
- Individual device creation per SIM card
- Seven sensor entities per SIM:
  - ICCID sensor
  - Status sensor
  - Plan name sensor
  - Expiry date sensor (with timestamp device class)
  - Data limit sensor (in GB)
  - Data remaining sensor (in GB)
  - Availability zone sensor
- Automatic data unit normalization (MB/KB to GB)
- Configuration flow with validation
- Reconfiguration support
- Automatic token refresh and authentication management
- HACS compatibility
- GitHub workflows for validation and releases

### Technical Details
- Built on Home Assistant's DataUpdateCoordinator pattern
- Uses aiohttp for async HTTP requests
- Implements proper error handling and logging
- Follows Home Assistant integration best practices
- Includes comprehensive device information
- Supports semantic versioning