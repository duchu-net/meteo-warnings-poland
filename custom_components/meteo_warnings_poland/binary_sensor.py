import asyncio
from datetime import datetime, timezone
import logging
from typing import Any, List, Mapping

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import parse_datetime

from .const import DOMAIN, PHENOMENON_CODES, PHENOMENONS, WARNINGS, WARNING_TYPES
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
    async_add_entities(entities)


class BinarySensor(BinarySensorEntity, SensorEntity):
    def __init__(self, coordinator: UpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)
        self._attr_entity_registry_enabled_default = False

    @property
    def device_class(self):
        return BinarySensorDeviceClass.SAFETY

    @property
    def unique_id(self):
        return f"{super().unique_id}_binary_sensor"


class WarningPresentBinarySensor(BinarySensor):
    def __init__(
        self,
        coordinator: UpdateCoordinator,
        config_entry: ConfigEntry,
        warning_type: str,
    ):
        super().__init__(coordinator, config_entry)
        self._warning_type = warning_type
        self._warning_key = WARNINGS[self._warning_type][0]

    @property
    def is_on(self) -> bool:
        level = int(self._warning_type)
        data = self.get_data()
        return (
            data is not None
            and level in data.by_level
            and len(data.by_level[level]) > 0
        )

    @property
    def available(self) -> bool:
        data = self.get_data()
        return super().available and data is not None and data.warnings is not None

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        level = int(self._warning_type)
        output["level"] = self._warning_key
        output["warnings"] = []

        data = self.get_data()
        if self.is_on and data is not None:
            output["warnings"] = data.get_level_dict(level)

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


def is_now_between(start: datetime, end: datetime):
    current_time = datetime.now(timezone.utc)
    # Ensure that start and end have the same time zone information
    start = start.replace(tzinfo=timezone.utc)
    end = end.replace(tzinfo=timezone.utc)
    return start <= current_time <= end


class WarningActiveBinarySensor(WarningPresentBinarySensor):
    def __init__(
        self,
        coordinator: UpdateCoordinator,
        config_entry: ConfigEntry,
        warning_type: str,
    ):
        super().__init__(coordinator, config_entry, warning_type)

    @property
    def is_on(self) -> bool:
        level = int(self._warning_type)
        data = self.get_data()
        if super().is_on and data is not None:
            warnings = data.get_level(level)
            warn = warnings[0]  # todo map over all warnings

            # start = warn.start_at
            # end = warn.end_at
            # return start <= datetime.datetime.now(tz=start.tzinfo) <= end  # type: ignore
            return is_now_between(warn.start_at, warn.end_at)
        return False

    async def async_update(self) -> None:
        await asyncio.sleep(0)

    @property
    def unique_id(self):
        return super().unique_id.replace("present", "active")

    @property
    def name(self):
        return f"{self.base_name()} {WARNINGS[self._warning_type][3]}"


""" 
PHENOMENONS SENSOR 
"""


class PhenomenonWarningPresentBinarySensor(BinarySensor):
    def __init__(
        self,
        coordinator: UpdateCoordinator,
        config_entry: ConfigEntry,
        phenomenon_code: str,
    ):
        super().__init__(coordinator, config_entry)
        self._phenomenon_type = phenomenon_code
        self._attr_entity_registry_enabled_default = False

    @property
    def is_on(self) -> bool:
        data = self.get_data()
        return (
            data is not None
            and self._phenomenon_type in data.by_phenomenon
            and len(data.by_phenomenon[self._phenomenon_type]) > 0
        )

    @property
    def available(self) -> bool:
        data = self.get_data()
        return super().available and data is not None and data.warnings is not None

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        phenomenon_code = self._phenomenon_type
        output["phenomenon"] = PHENOMENONS[self._phenomenon_type][0]
        output["warnings"] = []

        data = self.get_data()
        if self.is_on and data is not None:
            output["warnings"] = data.get_phenomenon_dict(phenomenon_code)

        return output

    @property
    def unique_id(self):
        return f"{super().unique_id}_present_{self._phenomenon_type.lower()}"

    # @property
    # def icon(self):
    #     return WARNINGS[self._phenomenon_type][1]

    @property
    def name(self):
        return f"{self.base_name()} {PHENOMENONS[self._phenomenon_type][0]}"
