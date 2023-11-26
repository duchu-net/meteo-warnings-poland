from datetime import timedelta
import datetime
import logging
from typing import Dict, List
from homeassistant.util import dt
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import requests

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

osmet_url = f"https://meteo.imgw.pl/api/meteo/messages/v1/osmet/latest/osmet-teryt"


# Parse IMGW API Dates format to UTC
def to_utc(date: str):
    return dt.as_utc(dt.parse_datetime(date))


def get_icon(level: int):
    if level > 0:
        return "mdi:alert"
    return "mdi:check-circle"


def get_color(level: int):
    if level > 1:
        return "var(--error-color)"
    if level > 0:
        return "var(--warning-color)"
    if level > -1:
        return "var(--success-color)"
    if level > -2:
        return "var(--info-color)"


class WarnData:
    def __init__(self):
        self.id: str = ""
        self.level: int = -2
        self.probability: int = -1
        self.forecaster: str = ""
        # Local formatted
        self.from_str: str
        self.to_str: str
        # UTC format
        # self.from: datetime
        self.to: datetime
        self.created_at: datetime
        # todo Content - comes also with eng text
        self.code: str
        self.phenomenon: str
        self.content: str | None = None
        self.comments: str
        self.short: str  # no eng version
        # UI
        self.icon_color: str


class IntegrationData:
    def __init__(self):
        self.warnings: List[WarnData] | None = None
        self.updated_at: datetime | None = None
        # self.ostrzezenia_pogodowe: Dict[str, str | int] | None = None
        # self.szukaj_burzy: Dict[str, str | int | float] | None = None
        # self.promieniowanie: float | None = None


class Connector:
    def __init__(self, region_id: str):
        self._region_id = region_id
        # self._service: ServiceSelector | None = None
        # self._api_key = api_key
        # self._latitude = latitude
        # self._longitude = longitude
        # self._radius = radius

    # def get_service(self) -> ServiceSelector:
    #     if self._service is None:
    #         self._service = Client(WSDL_URL).service
    #     return self._service

    def call_service(self):
        return requests.get(osmet_url)

    def get_data(self):
        _LOGGER.debug("get_data")
        data = IntegrationData()
        data.warnings = None
        data.updated_at = dt.utcnow()
        try:
            response = self.call_service()

            _LOGGER.debug(f"Warnings Response Status Code: {response.status_code}")
            _LOGGER.debug(f"Warnings Response Headers: {response.headers}")
            # _LOGGER.debug(f"Warnings Response Content: {response.text}")

            warnings_data = response.json()
            # _LOGGER.debug("warnings_data:", warnings_data)

            region_warnings = warnings_data.get("teryt", {}).get(self._region_id, [])
            # _LOGGER.debug("region_warnings:", region_warnings)

            data.warnings = []
            _LOGGER.debug("region_warnings:")
            for warn_code in region_warnings:
                _LOGGER.debug("loop1")
                warn_data = warnings_data.get("warnings", {}).get(warn_code, {})
                _LOGGER.debug("loop2")
                level = int(warn_data.get("Level", -2))
                _LOGGER.debug("loop3")
                _LOGGER.debug(f"loop", warn_code)
                _LOGGER.debug(f"loop", level)
                _LOGGER.debug("loop4")

                warn = WarnData()
                warn.id = warn_code
                warn.level = level
                warn.content = warn_data.get("Content")
                warn.phenomenon = warn_data.get("PhenomenonName")
                data.warnings.append(warn)
                _LOGGER.debug("loop5")
                _LOGGER.debug(len(data.warnings))
                # all_warnings.append(
                #     {
                #         "id": warn_code,
                #         "level": level,
                #         "probability": int(warn_data.get("Probability", 0)),
                #         "forecaster": warn_data.get("Name2"),
                #         # Local formatted
                #         "from_str": warn_data.get("ValidFrom"),
                #         "to_str": warn_data.get("ValidTo"),
                #         # UTC format
                #         "from": to_utc(warn_data.get("LxValidFrom")),
                #         "to": to_utc(warn_data.get("LxValidTo")),
                #         "created_at": to_utc(warn_data.get("LxReleaseDateTime")),
                #         #  todo Content - comes also with eng text
                #         "code": warn_data.get("PhenomenonCode"),
                #         "phenomenon": warn_data.get("PhenomenonName"),
                #         "content": warn_data.get("Content"),
                #         "comments": warn_data.get("Comments"),
                #         "short": warn_data.get("SMS"),  # no eng version
                #         # UI
                #         "icon_color": get_color(level),
                #     }
                # )

            # latitude = self.convert_to_dm(self._latitude)
            # longitude = self.convert_to_dm(self._longitude)
            # data.ostrzezenia_pogodowe = service.ostrzezenia_pogodowe(
            #     latitude, longitude, self._api_key
            # )
            # data.promieniowanie = service.promieniowanie(self._api_key)
            # data.szukaj_burzy = service.szukaj_burzy(
            #     latitude, longitude, self._radius, self._api_key
            # )
        except Exception as err:
            _LOGGER.error("Error while downloading data from imgw - connector", err)
        # except WebFault as fault:
        #     _LOGGER.error("Error while downloading data from burze.dzis.net: {}", fault)
        return data


class UpdateCoordinator(DataUpdateCoordinator[IntegrationData]):
    def __init__(
        self,
        hass: HomeAssistant,
        region_id: str,
        update_interval=DEFAULT_UPDATE_INTERVAL,
        # api_key: str,
        # latitude: float,
        # longitude: float,
        # radius: int,
    ):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
            update_method=self.update_method,
        )
        self.connector = Connector(region_id)

    # async def _async_update_data(self):
    #     try:
    #         # Note: asyncio.TimeoutError and aiohttp.ClientError are already
    #         # handled by the data update coordinator.
    #         async with async_timeout.timeout(10):
    #             # Grab active context variables to limit data required to be fetched from API
    #             # Note: using context is not required if there is no need or ability to limit
    #             # data retrieved from API.
    #             listening_idx = set(self.async_contexts())
    #             return await self._api.fetch_data(listening_idx)
    #             # return await self.connector.get_data()
    #     except:
    #         _LOGGER.error("Error while downloading data from imgw - coordinator")
    #     # except ApiAuthError as err:
    #     #     # Raising ConfigEntryAuthFailed will cancel future updates
    #     #     # and start a config flow with SOURCE_REAUTH (async_step_reauth)
    #     #     raise ConfigEntryAuthFailed from err
    #     # except ApiError as err:
    #     #     raise UpdateFailed(f"Error communicating with API: {err}")

    async def update_method(self) -> IntegrationData:
        return await self.hass.async_add_executor_job(self._update)

    def _update(self) -> IntegrationData:
        return self.connector.get_data()
