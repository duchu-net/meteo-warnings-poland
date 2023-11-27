import logging
from datetime import datetime, timedelta
from typing import Dict, List
import requests

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt

from .const import DEFAULT_UPDATE_INTERVAL, DOMAIN

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
    return ""


class WarnData:
    def __init__(self):
        self.id: str = ""
        self.level: int = -2
        self.probability: int = -1
        self.forecaster: str = ""
        # Local formatted
        self.start_str: str
        self.end_str: str
        # UTC format
        self.start_at: datetime
        self.end_at: datetime
        self.created_at: datetime
        #
        self.code: str
        self.phenomenon: str
        self.content: str | None = None
        self.comments: str
        self.short: str  # no eng version
        # UI
        self.icon_color: str


class IntegrationData:
    def __init__(self):
        self.updated_at: datetime | None = None
        self.warnings: List[WarnData] | None = None
        self.by_level: Dict[int, List[WarnData]] = {}
        self.by_phenomenon: Dict[str, List[WarnData]] = {}
        # self.ostrzezenia_pogodowe: Dict[str, str | int] | None = None
        # self.szukaj_burzy: Dict[str, str | int | float] | None = None
        # self.promieniowanie: float | None = None

    def get_level(self, level: int) -> List[WarnData]:
        warnings = []
        if level in self.by_level:
            for warn in self.by_level[level]:
                warnings.append(warn)
        return warnings

    def get_level_dict(self, level: int):
        warnings = []
        if level in self.by_level:
            for warn in self.by_level[level]:
                warnings.append(warn.__dict__)
        return warnings

    def get_phenomenon_dict(self, phenomenon_code: str):
        warnings = []
        if phenomenon_code in self.by_phenomenon:
            for warn in self.by_phenomenon[phenomenon_code]:
                warnings.append(warn.__dict__)
        return warnings

    def get_warnings_dict(self):
        warnings = []
        if self.warnings is not None:
            for warn in self.warnings:
                warnings.append(warn.__dict__)
        return warnings


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
            _LOGGER.debug(f"Warnings Response Content: {response.text}")

            warnings_data = response.json()
            region_warnings = warnings_data.get("teryt", {}).get(self._region_id, [])

            data.warnings = []
            for warn_code in region_warnings:
                warn_data = warnings_data.get("warnings", {}).get(warn_code, {})
                level = int(warn_data.get("Level", -2))
                code: str = warn_data.get("PhenomenonCode")

                # todo eng - content cames also with eng text, should be provided based on language
                warn = WarnData()
                warn.id = warn_code
                warn.level = level
                warn.probability = warn_data.get("Probability", 0)
                warn.code = code
                warn.phenomenon = warn_data.get("PhenomenonName")
                warn.forecaster = warn_data.get("Name2")
                warn.content = warn_data.get("Content")
                # Local formatted
                warn.start_str = warn_data.get("ValidFrom")
                warn.end_str = warn_data.get("ValidTo")
                # UTC format
                warn.start_at = to_utc(warn_data.get("LxValidFrom"))
                warn.end_at = to_utc(warn_data.get("LxValidTo"))
                warn.created_at = to_utc(warn_data.get("LxReleaseDateTime"))
                #
                warn.comments = warn_data.get("Comments")
                warn.short = warn_data.get("SMS")  # no eng version
                # UI
                warn.icon_color = get_color(level)

                # aggregated
                data.warnings.append(warn)
                # by level
                _LOGGER.debug(f"Level: {level}")
                # if data.by_level[level] is None:
                if level not in data.by_level:
                    data.by_level[level] = []
                data.by_level[level].append(warn)
                # by phenomenon
                if code not in data.by_phenomenon:
                    data.by_phenomenon[code] = []
                data.by_phenomenon[code].append(warn)
        except Exception as err:
            _LOGGER.error("Error while downloading data from imgw - connector", err)
        return data


class UpdateCoordinator(DataUpdateCoordinator[IntegrationData]):
    def __init__(
        self,
        hass: HomeAssistant,
        region_id: str,
        update_interval: timedelta,
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
