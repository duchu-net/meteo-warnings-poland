import logging
import json
from datetime import timedelta, datetime

import voluptuous as vol
import requests
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_NAME
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

from . import const

REGIONS = const.REGIONS
# TESTING ONLY
# from const import REGIONS

# Create a logger
logger = logging.getLogger(__name__)


# TESTING ONLY
# logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG
# # Create a console handler and set the level to DEBUG
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# # Create a formatter and attach it to the console handler
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# console_handler.setFormatter(formatter)
# # Add the console handler to the logger
# logger.addHandler(console_handler)

DOMAIN = "meteo_warnings_poland"
DEFAULT_NAME = "Meteo Warnings Poland"
CONF_REGION_ID = "region_id"
# CONF_REGION_IDS = "region_ids"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_REGION_ID): cv.string,
        # vol.Optional(CONF_REGION_IDS, default=[]): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
        # vol.Optional("update_interval", default=30): vol.All(vol.Coerce(int), vol.Range(min=10)),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Meteo Data sensor."""
    name = config.get(CONF_NAME)
    region_id = config[CONF_REGION_ID]
    # region_ids = config[CONF_REGION_IDS]
    # update_interval = config["update_interval"]

    # Create the Meteo Data sensors
    meteo_warnings_sensor = MeteoDataSensor(
        # name, region_id, region_ids, update_interval, "warnings"
        name,
        region_id,
        "warnings",
    )
    # meteo_dangers_sensor = MeteoDataSensor(
    #     name, region_id, region_ids, update_interval, "dangers"
    # )

    # Add the sensors to Home Assistant
    # add_entities([meteo_warnings_sensor, meteo_dangers_sensor], True)
    add_entities([meteo_warnings_sensor], True)


class MeteoDataSensor(Entity):
    # def __init__(self, name, region_id, region_ids, update_interval, data_type):
    def __init__(self, name, region_id, data_type):
        region_name = REGIONS[region_id]

        self._name = f"{name} {region_name.capitalize()}"
        self._region_id = region_id
        self._region_name = region_name
        # self._region_ids = region_ids
        # self._update_interval = timedelta(minutes=update_interval)
        self._data_type = data_type
        self._state = None
        self._attr = {"region": region_name}

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def device_class(self):
        return "number"

    @property
    def unit_of_measurement(self):
        return None  # todo get from translation "event/wydarzenie"

    @property
    def icon(self):
        return self.get_icon(self._state)

    @property
    def unique_id(self):
        return self._name

    @property
    def extra_state_attributes(self):
        return self._attr

    def get_icon(self, level):
        if level > 0:
            return "mdi:alert"
        return "mdi:check-circle"

    def get_color(self, level):
        if level > 1:
            return "var(--error-color)"
        if level > 0:
            return "var(--warning-color)"
        if level > -1:
            return "var(--success-color)"
        if level > -2:
            return "var(--info-color)"

    # @Throttle("update_interval")
    @Throttle(timedelta(minutes=10))
    def update(self):
        # async def async_update(self):
        self._attr["updated_at"] = datetime.now()
        try:
            all_warnings = []
            highest_level = -2
            logger.debug("init update")

            # OSMET
            osmet_response = requests.get(
                f"https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt"
            )
            logger.debug(f"Warnings Response Status Code: {osmet_response.status_code}")
            # logger.debug(f"Warnings Response Headers: {osmet_response.headers}")
            # logger.debug(f"Warnings Response Content: {osmet_response.text}")
            warnings_data = osmet_response.json()
            region_warnings = warnings_data.get("teryt", {}).get(self._region_id, [])
            for warn_code in region_warnings:
                warn_data = warnings_data.get("warnings", {}).get(warn_code, {})
                level = int(warn_data.get("Level", -2))
                all_warnings.append(
                    {
                        "level": level,
                        "probability": int(warn_data.get("Probability", 0)),
                        "forecaster": warn_data.get("Name2"),
                        # Dates:
                        "from": warn_data.get("LxValidFrom"),
                        "to": warn_data.get("LxValidTo"),
                        "created_at": warn_data.get("LxReleaseDateTime"),
                        #  todo Content - comes also with eng text
                        "phenomenon": warn_data.get("PhenomenonName"),
                        "content": warn_data.get("Content"),
                        "comments": warn_data.get("Comments"),
                        "short": warn_data.get("SMS"),  # no eng version
                        # UI
                        "icon_color": self.get_color(level),
                    }
                )

            # KOMET
            # todo - now its not returning data
            # komet_response = requests.get(
            #     f"https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/komet-teryt"
            # )
            # komet_data = komet_response.json().get("teryt", {}).get(self._region_id, [])

            # HYDRO
            # todo

            all_warnings.sort(key=lambda x: x["level"], reverse=True)
            for warn in all_warnings:  # todo get level of all_warnings first element xD
                if warn["level"] > highest_level:
                    highest_level = warn["level"]

            # Set the state based on the length of the warnings
            self._state = len(all_warnings)
            self._attr["level"] = highest_level
            self._attr["warnings"] = all_warnings
            self._attr["icon_color"] = self.get_color(highest_level)

        except Exception as ex:
            logger.error("Error fetching data: %s", ex)
            self._state = None
            self._attr["level"] = None
            self._attr["warnings"] = []
            self._attr["icon_color"] = None


# TESTING ONLY
# if __name__ == "__main__":
#     # Instantiate the sensor for testing
#     name = "Meteo Data"
#     region_id = "2201"
#     region_ids = ["additional_region_id_1", "additional_region_id_2"]
#     update_interval = 30  # Adjust as needed
#     data_type = "warnings"
#     test_sensor = MeteoDataSensor(name, region_id, region_ids, update_interval, data_type)
#     # Manually call the update method
#     test_sensor.update()
#     # Print the state and attributes
#     logger.info(f"State: {test_sensor.state}")
#     logger.info(f"Attributes: {test_sensor.extra_state_attributes}")
