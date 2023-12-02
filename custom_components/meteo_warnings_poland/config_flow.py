""" based on https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net """
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import selector
from homeassistant.const import CONF_UNIT_OF_MEASUREMENT, CONF_NAME

from .const import (
    CONF_ENABLED_SENSORS,
    CONF_REGION_ID,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL,
    DOMAIN,
    MIN_UPDATE_INTERVAL,
    REGIONS,
    SENSOR_CATEGORIES,
)

_LOGGER = logging.getLogger(__name__)

regions_sequence = sorted(
    [{"value": key, "label": value} for key, value in REGIONS.items()],
    key=lambda item: item["label"].lower(),
)
enabled_sequence = [
    {"value": key, "label": key.lower()} for key, value in SENSOR_CATEGORIES.items()
]

DATA_SCHEMA_FIRST_STEP = vol.Schema(
    {
        vol.Required(CONF_REGION_ID): selector(
            {
                "select": {
                    "options": regions_sequence,
                }
            }
        ),
        vol.Optional(CONF_NAME): selector({"text": {}}),
        # vol.Optional(
        #     CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL.total_seconds()
        # ): selector({"duration": {}}),
        vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): selector(
            {"number": {"min": 5, "max": 60, CONF_UNIT_OF_MEASUREMENT: "min"}}
        ),
        vol.Optional(CONF_ENABLED_SENSORS, default=["BASIC"]): selector(
            {"select": {"options": enabled_sequence, "multiple": True, "mode": "list"}}
        ),
    }
)


class FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._region_id: str
        self._name = None
        self._update_interval = None
        self._enabled_sensors = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            region_id = user_input[CONF_REGION_ID]
            name = user_input.get(CONF_NAME, None)
            update_interval = user_input[CONF_UPDATE_INTERVAL]
            enabled_sensors = user_input[CONF_ENABLED_SENSORS]
            _LOGGER.debug(f"entered region id: {region_id}, {name}, {update_interval}")

            if region_id in REGIONS:
                self._region_id = region_id
            else:
                errors[CONF_REGION_ID] = "invalid_region"

            if name:
                self._name = name
            else:
                self._name = None

            if update_interval >= MIN_UPDATE_INTERVAL:
                self._update_interval = update_interval
            else:
                errors[CONF_UPDATE_INTERVAL] = "invalid_interval"

            if len(enabled_sensors) > 0:
                self._enabled_sensors = enabled_sensors
            else:
                errors[CONF_ENABLED_SENSORS] = "empty_sensors"

            if len(errors) == 0:
                return await self.async_create_entry_from_fields()
                # return await self.async_step_use_home_location()

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA_FIRST_STEP, errors=errors
        )

    # async def async_step_use_home_location(self, user_input=None) -> FlowResult:
    #     if user_input is None:
    #         suggested_values: Mapping[str, Any] = {CONF_USE_HOME_COORDINATES: True}
    #         data_schema = self.add_suggested_values_to_schema(
    #             DATA_SCHEMA_USE_HOME_LOCATION, suggested_values
    #         )
    #         return self.async_show_form(
    #             step_id="use_home_location", data_schema=data_schema
    #         )

    #     self._use_home_coordinates = user_input[CONF_USE_HOME_COORDINATES]
    #     if self._use_home_coordinates:
    #         self._latitude = self.hass.config.latitude
    #         self._longitude = self.hass.config.longitude
    #         return await self.async_step_radius()
    #     else:
    #         return await self.async_step_location()

    # async def async_step_location(self, user_input=None) -> FlowResult:
    #     if user_input is None:
    #         suggested_values: Mapping[str, Any] = {
    #             CONF_LOCATION: {
    #                 CONF_LATITUDE: self.hass.config.latitude,
    #                 CONF_LONGITUDE: self.hass.config.longitude,
    #             }
    #         }
    #         data_schema = self.add_suggested_values_to_schema(
    #             DATA_SCHEMA_LOCATION, suggested_values
    #         )
    #         return self.async_show_form(step_id="location", data_schema=data_schema)

    #     self._longitude = user_input[CONF_LOCATION][CONF_LONGITUDE]
    #     self._latitude = user_input[CONF_LOCATION][CONF_LATITUDE]
    #     return await self.async_step_radius()

    # async def async_step_radius(self, user_input=None) -> FlowResult:
    #     if user_input is None:
    #         suggested_values: Mapping[str, Any] = {CONF_RADIUS: DEFAULT_RADIUS_IN_KM}
    #         data_schema = self.add_suggested_values_to_schema(
    #             DATA_SCHEMA_RADIUS, suggested_values
    #         )
    #         return self.async_show_form(step_id="radius", data_schema=data_schema)
    #     self._radius = user_input[CONF_RADIUS]
    #     return await self.async_create_entry_from_fields()

    async def async_create_entry_from_fields(self):
        title = f"Powiat {REGIONS[self._region_id]}"
        return self.async_create_entry(
            title=title,
            data={
                CONF_REGION_ID: self._region_id,
                CONF_NAME: self._name,
                CONF_UPDATE_INTERVAL: self._update_interval,
                CONF_ENABLED_SENSORS: self._enabled_sensors,
            },
        )
