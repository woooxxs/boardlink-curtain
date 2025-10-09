"""The Boardlink Curtain integration."""
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.COVER]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Boardlink Curtain component from YAML configuration."""
    hass.data[DOMAIN] = {}
    
    # Check if there is YAML configuration
    if DOMAIN in config:
        # Store YAML configuration for later use in config flow
        hass.data[DOMAIN]["yaml_config"] = config[DOMAIN]
    
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Boardlink Curtain from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # 存储配置项数据
    hass.data[DOMAIN][entry.entry_id] = dict(entry.data)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok