from dataclasses import dataclass
import logging
from datetime import datetime, timedelta, timezone
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


def is_now_between(start: datetime, end: datetime):
    current_time = datetime.now(timezone.utc)
    # Ensure that start and end have the same time zone information
    start = start.replace(tzinfo=timezone.utc)
    end = end.replace(tzinfo=timezone.utc)
    return start <= current_time <= end


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


# @dataclass
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


class Connector:
    def __init__(self, region_id: str):
        self._region_id = region_id
        # self._api_key = api_key

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
    ):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
            update_method=self.update_method,
        )
        self.connector = Connector(region_id)
        self._region_id = region_id

    @property
    def region_id(self):
        return self._region_id

    async def update_method(self) -> IntegrationData:
        return await self.hass.async_add_executor_job(self._update)

    def _update(self) -> IntegrationData:
        return self.connector.get_data()

    """ Utils """

    def get_all(self, active: bool = False) -> List[WarnData]:
        warnings = self.data.warnings
        if warnings is not None:
            if active:
                return UpdateCoordinator.select_active(warnings)
            return warnings
        return []

    def get_by_level(self, level: int, active: bool = False) -> List[WarnData]:
        by_level = self.data.by_level
        if level in by_level:
            if active:
                return UpdateCoordinator.select_active(by_level[level])
            return by_level[level]
        return []

    def get_by_phenomenon(
        self, phenomenon_code: str, active: bool = False
    ) -> List[WarnData]:
        by_phenomenon = self.data.by_phenomenon
        if phenomenon_code in by_phenomenon:
            if active:
                return UpdateCoordinator.select_active(by_phenomenon[phenomenon_code])
            return by_phenomenon[phenomenon_code]
        return []

    @staticmethod
    def select_active(data: List[WarnData]) -> List[WarnData]:
        warnings = []
        for warn in data:
            if is_now_between(warn.start_at, warn.end_at):
                warnings.append(warn)
        return warnings
