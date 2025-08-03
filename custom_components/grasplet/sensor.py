"""Sensor platform for Grasplet integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MANUFACTURER
from .coordinator import GraspletDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Grasplet sensor entities."""
    coordinator: GraspletDataUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = []
    
    if coordinator.data:
        for sim_data in coordinator.data:
            sim_id = str(sim_data["id"])
            sim_name = sim_data.get("name", f"SIM {sim_id}").strip()
            
            # Create entities for each SIM
            entities.extend([
                GraspletICCIDSensor(coordinator, sim_data, sim_id, sim_name),
                GraspletStatusSensor(coordinator, sim_data, sim_id, sim_name),
                GraspletPlanNameSensor(coordinator, sim_data, sim_id, sim_name),
                GraspletExpiryDateSensor(coordinator, sim_data, sim_id, sim_name),
                GraspletDataLimitSensor(coordinator, sim_data, sim_id, sim_name),
                GraspletDataRemainingSensor(coordinator, sim_data, sim_id, sim_name),
                GraspletDataUsagePercentageSensor(coordinator, sim_data, sim_id, sim_name),
                GraspletAvailabilityZoneSensor(coordinator, sim_data, sim_id, sim_name),
            ])
    
    async_add_entities(entities)


class GraspletSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Grasplet sensors."""
    
    def __init__(
        self,
        coordinator: GraspletDataUpdateCoordinator,
        sim_data: dict[str, Any],
        sim_id: str,
        sim_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sim_id = sim_id
        self._sim_name = sim_name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, sim_id)},
            name=sim_name,
            manufacturer=MANUFACTURER,
            model="Data SIM",
            sw_version="1.0",
        )

    @property
    def sim_data(self) -> dict[str, Any] | None:
        """Get the current SIM data."""
        if not self.coordinator.data:
            return None
            
        for sim in self.coordinator.data:
            if str(sim["id"]) == self._sim_id:
                return sim
        return None

    @property
    def plan_data(self) -> dict[str, Any] | None:
        """Get the plan data for this SIM."""
        sim = self.sim_data
        if sim and sim.get("PlanUsageDetails"):
            return sim["PlanUsageDetails"][0]
        return None


class GraspletICCIDSensor(GraspletSensorBase):
    """ICCID sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the ICCID sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} ICCID"
        self._attr_unique_id = f"{sim_id}_iccid"
        self._attr_icon = "mdi:sim"

    @property
    def native_value(self) -> str | None:
        """Return the ICCID."""
        sim = self.sim_data
        return sim.get("iccid") if sim else None


class GraspletStatusSensor(GraspletSensorBase):
    """Status sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the status sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} Status"
        self._attr_unique_id = f"{sim_id}_status"
        self._attr_icon = "mdi:signal"

    @property
    def native_value(self) -> str | None:
        """Return the status."""
        sim = self.sim_data
        return sim.get("status") if sim else None


class GraspletPlanNameSensor(GraspletSensorBase):
    """Plan name sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the plan name sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} Plan"
        self._attr_unique_id = f"{sim_id}_plan_name"
        self._attr_icon = "mdi:package-variant"

    @property
    def native_value(self) -> str | None:
        """Return the plan name."""
        plan_data = self.plan_data
        if plan_data and "plan" in plan_data:
            return plan_data["plan"].get("planName")
        return None


class GraspletExpiryDateSensor(GraspletSensorBase):
    """Expiry date sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the expiry date sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} Expiry Date"
        self._attr_unique_id = f"{sim_id}_expiry_date"
        self._attr_device_class = SensorDeviceClass.TIMESTAMP
        self._attr_icon = "mdi:calendar-clock"

    @property
    def native_value(self) -> datetime | None:
        """Return the expiry date."""
        plan_data = self.plan_data
        if plan_data and "plan" in plan_data:
            expiry_str = plan_data["plan"].get("expiryDate")
            if expiry_str:
                try:
                    return datetime.fromisoformat(expiry_str.replace("Z", "+00:00"))
                except ValueError:
                    _LOGGER.warning("Failed to parse expiry date: %s", expiry_str)
        return None


class GraspletDataLimitSensor(GraspletSensorBase):
    """Data limit sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the data limit sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} Data Limit"
        self._attr_unique_id = f"{sim_id}_data_limit"
        self._attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
        self._attr_device_class = SensorDeviceClass.DATA_SIZE
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_icon = "mdi:database"

    @property
    def native_value(self) -> float | None:
        """Return the data limit in GB."""
        plan_data = self.plan_data
        if plan_data and "plan" in plan_data:
            data_limit = plan_data["plan"].get("dataLimit")
            if data_limit is not None:
                return float(data_limit)
        return None


class GraspletDataRemainingSensor(GraspletSensorBase):
    """Data remaining sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the data remaining sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} Data Remaining"
        self._attr_unique_id = f"{sim_id}_data_remaining"
        self._attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
        self._attr_device_class = SensorDeviceClass.DATA_SIZE
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_suggested_display_precision = 3
        self._attr_icon = "mdi:download"

    @property
    def native_value(self) -> float | None:
        """Return the data remaining in GB."""
        plan_data = self.plan_data
        if plan_data and "usage" in plan_data:
            data_remaining = plan_data["usage"].get("data")
            data_unit = plan_data["usage"].get("dataUnit", "GB")
            
            if data_remaining is not None:
                # Normalize to GB
                if data_unit.upper() == "MB":
                    return float(data_remaining) / 1024
                elif data_unit.upper() == "KB":
                    return float(data_remaining) / (1024 * 1024)
                else:  # Assume GB
                    return float(data_remaining)
        return None


class GraspletAvailabilityZoneSensor(GraspletSensorBase):
    """Availability zone sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the availability zone sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} Availability Zone"
        self._attr_unique_id = f"{sim_id}_availability_zone"
        self._attr_icon = "mdi:earth"

    @property
    def native_value(self) -> str | None:
        """Return the availability zone."""
        plan_data = self.plan_data
        if plan_data and "usage" in plan_data:
            return plan_data["usage"].get("availabilityZone")
        return None


class GraspletDataUsagePercentageSensor(GraspletSensorBase):
    """Data usage percentage sensor."""
    
    def __init__(self, coordinator, sim_data, sim_id, sim_name):
        """Initialize the data usage percentage sensor."""
        super().__init__(coordinator, sim_data, sim_id, sim_name)
        self._attr_name = f"{sim_name} Data Usage %"
        self._attr_unique_id = f"{sim_id}_data_usage_percentage"
        self._attr_native_unit_of_measurement = "%"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:gauge"
        self._attr_suggested_display_precision = 1

    @property
    def native_value(self) -> float | None:
        """Return the data usage percentage."""
        plan_data = self.plan_data
        if plan_data and "plan" in plan_data and "usage" in plan_data:
            data_limit = plan_data["plan"].get("dataLimit")
            data_remaining = plan_data["usage"].get("data")
            data_unit = plan_data["usage"].get("dataUnit", "GB")
            
            if data_limit is not None and data_remaining is not None:
                # Normalize both to GB
                limit_gb = float(data_limit)
                remaining_gb = float(data_remaining)
                
                # Normalize remaining data to GB if needed
                if data_unit.upper() == "MB":
                    remaining_gb = remaining_gb / 1024
                elif data_unit.upper() == "KB":
                    remaining_gb = remaining_gb / (1024 * 1024)
                
                # Calculate used data
                used_gb = limit_gb - remaining_gb
                
                if limit_gb > 0 and used_gb >= 0:
                    return min(100.0, (used_gb / limit_gb) * 100)
        return None