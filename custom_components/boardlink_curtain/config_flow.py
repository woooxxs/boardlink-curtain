"""Config flow for Boardlink Curtain integration."""
import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    CONF_CLOSE_CODE,
    CONF_CLOSE_TIME,
    CONF_OPEN_CODE,
    CONF_PAUSE_CODE,
    DEFAULT_CLOSE_TIME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class BoardlinkCurtainConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Boardlink Curtain."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # 验证输入
            if not user_input.get("name"):
                errors["name"] = "名称不能为空"
            elif not user_input.get(CONF_OPEN_CODE):
                errors["open_code"] = "开帘红外码不能为空"
            elif not user_input.get(CONF_CLOSE_CODE):
                errors["close_code"] = "关帘红外码不能为空"
            elif not user_input.get(CONF_PAUSE_CODE):
                errors["pause_code"] = "暂停红外码不能为空"
            
            if not errors:
                # 检查设备名称是否已存在
                existing_entries = self.hass.config_entries.async_entries(DOMAIN)
                if any(entry.title == user_input["name"] for entry in existing_entries):
                    errors["name"] = "该设备名称已存在"
                else:
                    # 创建配置项
                    return self.async_create_entry(
                        title=user_input["name"],
                        data=user_input,
                    )

        # 默认值
        data_schema = vol.Schema({
            vol.Required("name", default="窗帘"): str,
            vol.Required(CONF_OPEN_CODE, default="send_open"): str,
            vol.Required(CONF_CLOSE_CODE, default="send_close"): str,
            vol.Required(CONF_PAUSE_CODE, default="send_stop"): str,
            vol.Required(CONF_CLOSE_TIME, default=DEFAULT_CLOSE_TIME): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_import(self, import_data: dict[str, Any]) -> FlowResult:
        """Handle import from YAML configuration."""
        return await self.async_step_user(import_data)

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return BoardlinkCurtainOptionsFlowHandler(config_entry)


class BoardlinkCurtainOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Boardlink Curtain."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        errors = {}

        if user_input is not None:
            # 验证输入
            if not user_input.get(CONF_OPEN_CODE):
                errors["open_code"] = "开帘红外码不能为空"
            elif not user_input.get(CONF_CLOSE_CODE):
                errors["close_code"] = "关帘红外码不能为空"
            elif not user_input.get(CONF_PAUSE_CODE):
                errors["pause_code"] = "暂停红外码不能为空"
            
            if not errors:
                # 更新配置项
                return self.async_create_entry(
                    title="",
                    data=user_input,
                )

        # 获取当前配置
        current_data = self.config_entry.data

        # 默认值
        data_schema = vol.Schema({
            vol.Required("name", default=current_data.get("name", "窗帘")): str,
            vol.Required(CONF_OPEN_CODE, default=current_data.get(CONF_OPEN_CODE, "send_open")): str,
            vol.Required(CONF_CLOSE_CODE, default=current_data.get(CONF_CLOSE_CODE, "send_close")): str,
            vol.Required(CONF_PAUSE_CODE, default=current_data.get(CONF_PAUSE_CODE, "send_stop")): str,
            vol.Required(CONF_CLOSE_TIME, default=current_data.get(CONF_CLOSE_TIME, DEFAULT_CLOSE_TIME)): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema,
            errors=errors,
        )