from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, CONF_REGION_ID, DEFAULT_NAME, DOMAIN, REGIONS
from .coordinator import IntegrationData, UpdateCoordinator


class SensorEntity(CoordinatorEntity):
    def __init__(self, coordinator: UpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator)
        self.config_entry = config_entry

    @property
    def extra_state_attributes(self) -> dict:
        return {ATTR_ATTRIBUTION: ATTRIBUTION}

    def get_data(self) -> IntegrationData | None:
        return self.coordinator.data

    @property
    def name(self):
        return self.base_name()

    def base_name(self):
        # if self.config_entry.data[CONF_USE_HOME_COORDINATES]:
        #     return DEFAULT_NAME
        region_id = self.config_entry.data[CONF_REGION_ID]
        return f"{DEFAULT_NAME} ({REGIONS[region_id]})"

    @property
    def unique_id(self):
        # if self.config_entry.data[CONF_USE_HOME_COORDINATES]:
        #     return f"{DOMAIN}_home"
        region_id = self.config_entry.data[CONF_REGION_ID]
        return f"{DOMAIN}_{REGIONS[region_id]}"

    @property
    def device_info(self):
        region_id = self.config_entry.data[CONF_REGION_ID]
        return {
            "identifiers": {(DOMAIN, REGIONS[region_id])},
            "name": self.base_name(),
        }
