"""Data update coordinator for Grasplet integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_POLL_INTERVAL, DATA_URL, DOMAIN, LOGIN_URL

_LOGGER = logging.getLogger(__name__)


class GraspletDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from Grasplet API."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.entry = entry
        self._access_token: str | None = None
        self._session: aiohttp.ClientSession | None = None
        
        update_interval = timedelta(hours=entry.data[CONF_POLL_INTERVAL])
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_setup(self) -> None:
        """Set up the coordinator."""
        self._session = aiohttp.ClientSession()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Grasplet API."""
        if self._session is None:
            await self._async_setup()

        try:
            # Authenticate if we don't have a token
            if not self._access_token:
                await self._authenticate()
            
            # Fetch SIM data
            return await self._fetch_sim_data()
            
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            _LOGGER.exception("Unexpected error fetching data")
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def _authenticate(self) -> None:
        """Authenticate with Grasplet API."""
        if self._session is None:
            raise UpdateFailed("Session not initialized")
            
        payload = {
            "username": self.entry.data[CONF_USERNAME],
            "password": self.entry.data[CONF_PASSWORD],
        }
        
        # Mask password in logs
        _LOGGER.debug("Authenticating with username: %s", payload["username"])
        
        try:
            async with self._session.post(LOGIN_URL, json=payload) as response:
                if response.status == 201:
                    result = await response.json()
                    if result.get("result") and "access_token" in result.get("data", {}):
                        self._access_token = result["data"]["access_token"]
                        _LOGGER.debug("Authentication successful")
                        return
                
                _LOGGER.error("Authentication failed with status: %s", response.status)
                if response.status == 401:
                    raise ConfigEntryAuthFailed("Invalid credentials")
                raise UpdateFailed(f"Authentication failed: {response.status}")
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error during authentication: %s", err)
            raise UpdateFailed(f"Authentication failed: {err}") from err

    async def _fetch_sim_data(self) -> dict[str, Any]:
        """Fetch SIM data from Grasplet API."""
        if not self._access_token:
            raise UpdateFailed("No access token available")
            
        if self._session is None:
            raise UpdateFailed("Session not initialized")
            
        headers = {"Authorization": f"Bearer {self._access_token}"}
        
        try:
            async with self._session.get(DATA_URL, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get("result") and "data" in result:
                        _LOGGER.debug("Successfully fetched data for %d SIMs", len(result["data"]))
                        return result["data"]
                
                if response.status == 401:
                    # Token expired, clear it and try to re-authenticate
                    self._access_token = None
                    _LOGGER.info("Access token expired, will re-authenticate on next update")
                    raise UpdateFailed("Access token expired")
                
                _LOGGER.error("Failed to fetch SIM data with status: %s", response.status)
                raise UpdateFailed(f"Failed to fetch data: {response.status}")
                
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error fetching SIM data: %s", err)
            raise UpdateFailed(f"Failed to fetch data: {err}") from err

    async def async_shutdown(self) -> None:
        """Close the session when shutting down."""
        if self._session:
            await self._session.close()
            self._session = None