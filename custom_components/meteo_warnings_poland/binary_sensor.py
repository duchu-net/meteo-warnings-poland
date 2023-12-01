import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from typing import Any, List, Mapping

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.components.sensor import (
    DOMAIN as PLATFORM,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import parse_datetime
from homeassistant.helpers.update_coordinator import CoordinatorEntity


from .const import DOMAIN, NAMES, PHENOMENON_CODES, PHENOMENONS, WARNINGS, WARNING_TYPES
from .coordinator import UpdateCoordinator, WarnData
from .entity import SensorEntity

_LOGGER = logging.getLogger(__name__)


def contains_object_with_key(objects, key):
    for obj in objects:
        if key in obj:
            return True
    return False


def count_objects_with_level(objects: List[WarnData], level: int) -> int:
    count = 0
    for obj in objects:
        if obj.level == level:
            count += 1
    return count


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator: UpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for warning_type in WARNING_TYPES:
        entities.append(WarningPresentBinarySensor(coordinator, entry, warning_type))
        entities.append(WarningActiveBinarySensor(coordinator, entry, warning_type))
    for phenomenon_code in PHENOMENON_CODES:
        entities.append(
            PhenomenonWarningPresentBinarySensor(coordinator, entry, phenomenon_code)
        )
        entities.append(
            PhenomenonWarningActiveBinarySensor(coordinator, entry, phenomenon_code)
        )
    async_add_entities(entities)


class MWPBinarySensor(BinarySensorEntity, SensorEntity):
    def __init__(self, coordinator: UpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._attr_entity_registry_enabled_default = False

    @property
    def device_class(self):
        return BinarySensorDeviceClass.SAFETY

    @property
    def unique_id(self):
        return f"{super().unique_id}_binary_sensor"


class WarningPresentBinarySensor(MWPBinarySensor):
    def __init__(
        self,
        coordinator: UpdateCoordinator,
        config_entry: ConfigEntry,
        warning_type: str,
    ):
        super().__init__(coordinator, config_entry)
        self._warning_type = warning_type
        self._warning_level = int(self._warning_type)

    @property
    def is_on(self) -> bool:
        return len(self.coordinator.get_by_level(self._warning_level)) > 0

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        output["level"] = self._warning_level
        output["warnings"] = []
        if self.is_on:
            output["warnings"] = [
                x.__dict__ for x in self.coordinator.get_by_level(self._warning_level)
            ]

        return output

    @property
    def unique_id(self):
        return f"{super().unique_id}_present_{self._warning_type}"

    @property
    def icon(self):
        return WARNINGS[self._warning_type][1]

    @property
    def name(self):
        return f"{self.base_name()} {WARNINGS[self._warning_type][2]}"


class WarningActiveBinarySensor(WarningPresentBinarySensor):
    async def async_update(self) -> None:
        await asyncio.sleep(0)

    @property
    def is_on(self) -> bool:
        if super().is_on:
            return len(self.coordinator.get_by_level(self._warning_level, True)) > 0
        return False

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        output["level"] = self._warning_level
        output["warnings"] = []
        if self.is_on:
            output["warnings"] = [
                x.__dict__
                for x in self.coordinator.get_by_level(self._warning_level, True)
            ]

        return output

    @property
    def unique_id(self):
        return super().unique_id.replace("present", "active")

    @property
    def name(self):
        return f"{self.base_name()} {WARNINGS[self._warning_type][3]}"


""" 
PHENOMENONS SENSOR 
"""


class PhenomenonWarningPresentBinarySensor(MWPBinarySensor):
    def __init__(
        self,
        coordinator: UpdateCoordinator,
        config_entry: ConfigEntry,
        phenomenon_code: str,
    ):
        super().__init__(coordinator, config_entry)
        self._phenomenon_code = phenomenon_code
        self._phenomenon_name = PHENOMENONS[self._phenomenon_code][0]
        self._attr_entity_registry_enabled_default = False

    @property
    def is_on(self) -> bool:
        return len(self.coordinator.get_by_phenomenon(self._phenomenon_code)) > 0

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        output["phenomenon"] = self._phenomenon_name
        output["warnings"] = []
        if self.is_on:
            output["warnings"] = [
                x.__dict__
                for x in self.coordinator.get_by_phenomenon(self._phenomenon_code)
            ]

        return output

    @property
    def unique_id(self):
        return f"{super().unique_id}_present_{self._phenomenon_code.lower()}"

    @property
    def icon(self):
        return PHENOMENONS[self._phenomenon_code][2]

    @property
    def name(self):
        return (
            f"{self.base_name()} {self._phenomenon_name} {NAMES['PresentPhenomenon']}"
        )


class PhenomenonWarningActiveBinarySensor(PhenomenonWarningPresentBinarySensor):
    @property
    def is_on(self) -> bool:
        return len(self.coordinator.get_by_phenomenon(self._phenomenon_code, True)) > 0

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        output["warnings"] = []
        if self.is_on:
            output["warnings"] = [
                x.__dict__
                for x in self.coordinator.get_by_phenomenon(self._phenomenon_code, True)
            ]

        return output

    @property
    def unique_id(self):
        return super().unique_id.replace("present", "active")

    @property
    def name(self):
        return f"{self.base_name()} {self._phenomenon_name} {NAMES['ActivePhenomenon']}"
