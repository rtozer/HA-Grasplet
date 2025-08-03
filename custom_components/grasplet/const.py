"""Constants for the Grasplet integration."""

DOMAIN = "grasplet"

# Configuration keys
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_POLL_INTERVAL = "poll_interval"

# Default values
DEFAULT_POLL_INTERVAL = 24  # hours

# API URLs
BASE_URL = "https://data.grasplet.com"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
DATA_URL = f"{BASE_URL}/api/sim/all"

# Device info
MANUFACTURER = "Grasplet"