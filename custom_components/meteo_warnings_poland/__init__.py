import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_REGION_ID, DOMAIN, PLATFORMS
from .coordinator import UpdateCoordinator

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_REGION_ID): cv.string,
        # vol.Optional(CONF_REGION_IDS, default=[]): vol.All(cv.ensure_list, [cv.string]),
        # vol.Optional(CONF_NANE, default=DEFAULT_NAME): str,
        # vol.Optional("update_interval", default=30): vol.All(vol.Coerce(int), vol.Range(min=10)),
    }
)


async def async_setup(hass, config):
    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    region_id = config_entry.data.get(CONF_REGION_ID)
    # api_key = config_entry.data.get(CONF_API_KEY)
    # longitude = config_entry.data.get(CONF_LONGITUDE)
    # latitude = config_entry.data.get(CONF_LATITUDE)
    # radius = config_entry.data.get(CONF_RADIUS)

    coordinator = UpdateCoordinator(hass, region_id)
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][config_entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    config_entry.async_on_unload(config_entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a config entry."""
    unloaded = await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(config_entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
