import logging
from typing import Any, List, Mapping

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util.dt import parse_datetime
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN, WARNING_TYPES
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
    for warning_type in WARNING_TYPES.keys():
        entities.append(WarningPresentBinarySensor(coordinator, entry, warning_type))
        # entities.append(
        #     BurzeDzisNetWarningActiveBinarySensor(coordinator, entry, warning_type)
        # )
    # entities.append(BurzeDzisNetStormNearbyBinarySensor(coordinator, entry))
    async_add_entities(entities)


class BinarySensor(BinarySensorEntity, SensorEntity):
    def __init__(self, coordinator: UpdateCoordinator, config_entry: ConfigEntry):
        super().__init__(coordinator, config_entry)

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
        self._warning_key = WARNING_TYPES[self._warning_type][0]

    @property
    def is_on(self) -> bool:
        data = self.get_data()
        return (
            data is not None
            and data.warnings is not None
            and count_objects_with_level(data.warnings, int(self._warning_type)) > 0
        )

    @property
    def available(self) -> bool:
        data = self.get_data()
        return super().available and data is not None and data.warnings is not None

    @property
    def extra_state_attributes(self) -> Mapping[str, Any]:
        output = super().extra_state_attributes
        output["level"] = self._warning_key
        output["warnings"] = []

        warnings = self.get_data().warnings
        if self.is_on and warnings is not None:
            for warn in warnings:
                if int(self._warning_type) == warn.level:
                    output["warnings"].append(warn.__dict__)
        # output["description"] = WARNING_DESCRIPTIONS[self._warning_type][
        #     data[self._warning_key]
        # ]
        # output["from"] = str(
        #     parse_datetime(data[self._warning_key + "_od_dnia"] + "Z")
        # )
        # output["to"] = str(
        #     parse_datetime(data[self._warning_key + "_do_dnia"] + "Z")
        # )
        return output

    @property
    def unique_id(self):
        return f"{super().unique_id}_warning_present_{self._warning_type}"

    @property
    def icon(self):
        return WARNING_TYPES[self._warning_type][1]

    @property
    def name(self):
        return f"{self.base_name()} {WARNING_TYPES[self._warning_type][2]}"


# class BurzeDzisNetWarningActiveBinarySensor(WarningPresentBinarySensor):
#     def __init__(
#         self,
#         coordinator: UpdateCoordinator,
#         config_entry: ConfigEntry,
#         warning_type: str,
#     ):
#         super().__init__(coordinator, config_entry, warning_type)

#     @property
#     def is_on(self) -> bool:
#         is_present = super().is_on
#         if is_present:
#             data = self.get_data().ostrzezenia_pogodowe
#             start = parse_datetime(data[self._warning_key + "_od_dnia"] + "Z")
#             end = parse_datetime(data[self._warning_key + "_do_dnia"] + "Z")
#             return start <= datetime.datetime.now(tz=start.tzinfo) <= end
#         return False

#     def should_poll(self) -> bool:
#         return True

#     async def async_update(self) -> None:
#         await asyncio.sleep(0)

#     @property
#     def unique_id(self):
#         return super().unique_id.replace("present", "active")

#     @property
#     def name(self):
#         return f"{self.base_name()} {WARNING_TYPES[self._warning_type][3]}"


# class BurzeDzisNetStormNearbyBinarySensor(BinarySensor):
#     def __init__(
#         self, coordinator: UpdateCoordinator, config_entry: ConfigEntry
#     ):
#         super().__init__(coordinator, config_entry)

#     @property
#     def is_on(self):
#         data = self.get_data()
#         return (
#             data is not None
#             and data.szukaj_burzy is not None
#             and data.szukaj_burzy["liczba"] > 0
#         )

#     @property
#     def extra_state_attributes(self) -> dict:
#         output = super().extra_state_attributes
#         if self.is_on:
#             data = self.get_data().szukaj_burzy
#             output["number"] = data["liczba"]
#             output["distance"] = data["odleglosc"]
#             output["direction"] = data["kierunek"]
#             output["period"] = data["okres"]
#         return output

#     @property
#     def available(self) -> bool:
#         return (
#             super().available
#             and self.get_data() is not None
#             and self.get_data().szukaj_burzy is not None
#         )

#     @property
#     def name(self):
#         return f"{self.base_name()} {STORM_NEARBY[1]}"

#     @property
#     def icon(self):
#         return STORM_NEARBY[0]

#     @property
#     def unique_id(self):
#         return f"{super().unique_id}_storm_nearby"
