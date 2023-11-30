import logging
from typing import Any, Mapping

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, WARNING_TYPES, WARNINGS
from .coordinator import UpdateCoordinator
from .entity import SensorEntity as MWPSensorEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    coordinator: UpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    """ Ogłoszony z nazwami zjawisk """
    entities.append(MWPPresentWarningSensor(coordinator, entry))
    """ Aktywny z nazwami zjawisk """
    entities.append(MWPActiveWarningSensor(coordinator, entry))
    for warning_type in WARNING_TYPES:
        """Ogłoszony dla poziomu z nazwami zjawisk"""
        entities.append(MWPPresentWarningLevelSensor(coordinator, entry, warning_type))
        """ Aktywny dla poziomu z nazwami zjawisk """
        entities.append(MWPActiveWarningLevelSensor(coordinator, entry, warning_type))
    async_add_entities(entities)


class MWPSensor(SensorEntity, MWPSensorEntity):
    def __init__(self, coordinator: UpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)

    @property
    def unique_id(self):
        return f"{super().unique_id}_sensor"


class MWPPresentWarningSensor(MWPSensor):
    def get_data(self):
        return self.coordinator.get_all()

    @property
    def native_value(self) -> str | None:
        warnings = self.get_data()
        if len(warnings) > 0:
            return ", ".join([x.phenomenon for x in warnings])
        return None

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        output["warnings"] = []
        if self.state is not None:
            output["warnings"] = [x.__dict__ for x in self.get_data()]
        return output

    @property
    def unique_id(self):
        return f"{super().unique_id}_present"

    @property
    def icon(self):
        if self.state is not None:
            return "mdi:alert-circle"
        return "mdi:check-circle"

    @property
    def name(self):
        return f"{self.base_name()} Ogłoszony Fenomen"


class MWPActiveWarningSensor(MWPPresentWarningSensor):
    def get_data(self):
        return self.coordinator.get_all(True)

    @property
    def unique_id(self):
        return super().unique_id.replace("present", "active")

    @property
    def name(self):
        return f"{self.base_name()} Aktywny Fenomen"


class MWPPresentWarningLevelSensor(MWPSensor):
    def __init__(
        self,
        coordinator: UpdateCoordinator,
        config_entry: ConfigEntry,
        warning_type: str,
    ):
        super().__init__(coordinator, config_entry)
        self._warning_type = warning_type
        self._warning_level = int(self._warning_type)

    def get_data(self):
        return self.coordinator.get_by_level(self._warning_level)

    @property
    def native_value(self) -> str | None:
        warnings = self.get_data()
        if len(warnings) > 0:
            return ", ".join([x.phenomenon for x in warnings])
        return None

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        output["level"] = self._warning_level
        output["warnings"] = []
        if self.state is not None:
            output["warnings"] = [x.__dict__ for x in self.get_data()]
        return output

    @property
    def unique_id(self):
        return f"{super().unique_id}_present_level_{self._warning_type}"

    @property
    def icon(self):
        return WARNINGS[self._warning_type][1]

    @property
    def name(self):
        return f"{self.base_name()} {WARNINGS[self._warning_type][4]}"


class MWPActiveWarningLevelSensor(MWPPresentWarningLevelSensor):
    def get_data(self):
        return self.coordinator.get_by_level(self._warning_level, True)

    @property
    def unique_id(self):
        return super().unique_id.replace("present", "active")

    @property
    def name(self):
        return f"{self.base_name()} {WARNINGS[self._warning_type][5]}"
