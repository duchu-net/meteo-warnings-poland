""" based on https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net """
import logging
from typing import Any, Mapping
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.selector import selector

from .const import CONF_REGION_ID, DEFAULT_NAME, DOMAIN, REGIONS

_LOGGER = logging.getLogger(__name__)

# DATA_SCHEMA_REGION_ID = vol.Schema({vol.Required(CONF_REGION_ID): str})
DATA_SCHEMA_REGION_ID = vol.Schema(
    {
        vol.Required(CONF_REGION_ID): selector(
            {
                "select": {
                    "options": sorted(list(REGIONS.values()), key=lambda x: x.lower()),
                }
            }
        ),
    }
)
# DATA_SCHEMA_API_KEY = vol.Schema({vol.Required(CONF_API_KEY): str})

# DATA_SCHEMA_USE_HOME_LOCATION = vol.Schema(
#     {vol.Required(CONF_USE_HOME_COORDINATES): bool}
# )

# DATA_SCHEMA_LOCATION = vol.Schema(
#     {
#         vol.Required(CONF_LOCATION): selector.LocationSelector(
#             selector.LocationSelectorConfig(radius=False, icon="mdi:radar")
#         ),
#     }
# )

# DATA_SCHEMA_RADIUS = vol.Schema({vol.Required(CONF_RADIUS): cv.positive_int})


class FlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    def __init__(self):
        self._region_id: str
        # self._api_key = None
        # self._latitude = None
        # self._longitude = None
        # self._use_home_coordinates = None
        # self._radius = None

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            region_name = user_input[CONF_REGION_ID]
            _LOGGER.debug("entered region id", region_name)

            found_id = None
            for key, value in REGIONS.items():
                if value == region_name:
                    found_id = key
                    break

            if found_id:
                self._region_id = found_id
                # return await self.async_step_use_home_location()
                return await self.async_create_entry_from_fields()
            else:
                errors[CONF_REGION_ID] = "invalid_region"
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA_REGION_ID, errors=errors
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
        # if self._use_home_coordinates:
        #     title = f"{DEFAULT_NAME}"
        # else:
        #     title = f"{DEFAULT_NAME} ({self._latitude:.2f}, {self._longitude:.2f})"
        title = f"{DEFAULT_NAME} ({REGIONS[self._region_id]})"
        return self.async_create_entry(
            title=title,
            data={
                CONF_REGION_ID: self._region_id,
                # CONF_API_KEY: self._api_key,
                # CONF_LATITUDE: self._latitude,
                # CONF_LONGITUDE: self._longitude,
                # CONF_USE_HOME_COORDINATES: self._use_home_coordinates,
                # CONF_RADIUS: self._radius,
            },
        )
