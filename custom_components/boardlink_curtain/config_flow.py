"""Config flow for Boardlink Curtain."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import device_registry as dr

from .const import (
    CONF_BROADLINK_DEVICE,
    CONF_BROADLINK_TYPE,
    CONF_CLOSE_CODE,
    CONF_CLOSE_TIME,
    CONF_OPEN_CODE,
    CONF_PAUSE_CODE,
    DEFAULT_CLOSE_TIME,
    DOMAIN,
    BROADLINK_TYPES,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): str,
        vol.Required(CONF_OPEN_CODE): str,
        vol.Required(CONF_CLOSE_CODE): str,
        vol.Required(CONF_PAUSE_CODE): str,
        vol.Optional(CONF_CLOSE_TIME, default=DEFAULT_CLOSE_TIME): vol.Coerce(int),
        vol.Optional(CONF_BROADLINK_DEVICE): str,
        vol.Optional(CONF_BROADLINK_TYPE, default="RM_MINI3"): vol.In(BROADLINK_TYPES),
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # 这里可以添加验证逻辑，比如检查代码格式等
    return {"title": data[CONF_NAME]}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Boardlink Curtain."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except HomeAssistantError:
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_NAME])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=info["title"], data=user_input)

        # 获取可用的Broadlink设备
        device_registry = dr.async_get(self.hass)
        broadlink_devices = []
        for device in device_registry.devices.values():
            if any("broadlink" in str(identifier).lower() for identifier in device.identifiers):
                device_name = next(iter(device.identifiers))[1] if device.identifiers else str(device.id)
                broadlink_devices.append(device_name)

        # 如果没有找到Broadlink设备，提供手动输入选项
        if not broadlink_devices:
            schema = vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_OPEN_CODE): str,
                    vol.Required(CONF_CLOSE_CODE): str,
                    vol.Required(CONF_PAUSE_CODE): str,
                    vol.Optional(CONF_CLOSE_TIME, default=DEFAULT_CLOSE_TIME): vol.Coerce(int),
                    vol.Optional(CONF_BROADLINK_DEVICE): str,
                    vol.Optional(CONF_BROADLINK_TYPE, default="RM_MINI3"): vol.In(BROADLINK_TYPES),
                }
            )
        else:
            schema = vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_OPEN_CODE): str,
                    vol.Required(CONF_CLOSE_CODE): str,
                    vol.Required(CONF_PAUSE_CODE): str,
                    vol.Optional(CONF_CLOSE_TIME, default=DEFAULT_CLOSE_TIME): vol.Coerce(int),
                    vol.Optional(CONF_BROADLINK_DEVICE): vol.In(broadlink_devices),
                    vol.Optional(CONF_BROADLINK_TYPE, default="RM_MINI3"): vol.In(BROADLINK_TYPES),
                }
            )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )