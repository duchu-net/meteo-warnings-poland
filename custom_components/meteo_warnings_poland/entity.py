from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType

from .const import (
    ATTRIBUTION,
    CONF_ENABLED_SENSORS,
    CONF_REGION_ID,
    DEFAULT_NAME,
    DOMAIN,
    IMGW_MANUFACTURER,
    REGIONS,
    SHORT_DOMAIN,
)
from .coordinator import IntegrationData, UpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class SensorEntity(CoordinatorEntity[UpdateCoordinator]):
    _category: str = "OTHER"

    def __init__(self, coordinator: UpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self._attr_entity_registry_enabled_default = (
            self._category in config_entry.data.get(CONF_ENABLED_SENSORS, [])
        )

    @property
    def extra_state_attributes(self) -> dict:
        return {
            ATTR_ATTRIBUTION: ATTRIBUTION,
            "updated_at": self.coordinator.data.updated_at,
        }

    def get_data(self) -> IntegrationData:
        return self.coordinator.data

    @property
    def available(self) -> bool:
        return super().available and self.coordinator.data.warnings is not None

    @property
    def name(self):
        return self.base_name()

    def base_name(self):
        name: str | None = self.config_entry.data.get(CONF_NAME)
        if name is not None:
            return name
        region_id = self.config_entry.data[CONF_REGION_ID]
        return f"{DEFAULT_NAME} {REGIONS[region_id]}"

    @property
    def unique_id(self):
        region_id = self.config_entry.data[CONF_REGION_ID]
        return f"{SHORT_DOMAIN}_{region_id}"

    @property
    def device_info(self):
        region_id = self.config_entry.data[CONF_REGION_ID]
        return DeviceInfo(
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, region_id)},
            manufacturer=IMGW_MANUFACTURER,
            model=f"IMGW-{REGIONS[region_id]}-{region_id}",
            name=self.base_name(),
        )
