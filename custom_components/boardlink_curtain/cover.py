"""Support for Boardlink Curtain devices."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.cover import (
    ATTR_POSITION,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    CONF_BROADLINK_DEVICE,
    CONF_BROADLINK_TYPE,
    CONF_CLOSE_CODE,
    CONF_CLOSE_TIME,
    CONF_OPEN_CODE,
    CONF_PAUSE_CODE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Boardlink Curtain cover."""
    data = config_entry.data
    
    async_add_entities(
        [
            BoardlinkCurtain(
                name=data[CONF_NAME],
                open_code=data[CONF_OPEN_CODE],
                close_code=data[CONF_CLOSE_CODE],
                pause_code=data[CONF_PAUSE_CODE],
                close_time=data.get(CONF_CLOSE_TIME, 30),
                broadlink_device=data.get(CONF_BROADLINK_DEVICE),
                broadlink_type=data.get(CONF_BROADLINK_TYPE, "RM_MINI3"),
                unique_id=config_entry.entry_id,
                hass=hass,
            )
        ]
    )


class BoardlinkCurtain(CoverEntity, RestoreEntity):
    """Representation of a Boardlink Curtain."""

    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.STOP
        | CoverEntityFeature.SET_POSITION
    )

    def __init__(
        self,
        name: str,
        open_code: str,
        close_code: str,
        pause_code: str,
        close_time: int,
        broadlink_device: str,
        broadlink_type: str,
        unique_id: str,
        hass: HomeAssistant,
    ) -> None:
        """Initialize the curtain."""
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._open_code = open_code
        self._close_code = close_code
        self._pause_code = pause_code
        self._close_time = close_time  # 完全关闭所需时间（秒）
        self._broadlink_device = broadlink_device
        self._broadlink_type = broadlink_type
        self._hass = hass
        
        # 0% = 完全开启, 100% = 完全关闭
        self._attr_current_cover_position = 0
        self._attr_is_closed = False
        self._attr_is_closing = False
        self._attr_is_opening = False
        
        # 用于模拟运动的任务
        self._movement_task: asyncio.Task | None = None

    async def async_added_to_hass(self) -> None:
        """Call when entity about to be added to hass."""
        await super().async_added_to_hass()
        
        # 恢复之前的状态
        if (last_state := await self.async_get_last_state()) is not None:
            if last_state.attributes.get(ATTR_POSITION) is not None:
                self._attr_current_cover_position = last_state.attributes[ATTR_POSITION]
                self._attr_is_closed = self._attr_current_cover_position == 100

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        if self._movement_task:
            self._movement_task.cancel()
            
        _LOGGER.info(f"Opening curtain {self.name} with code: {self._open_code}")
        
        # 这里可以添加发送红外码的逻辑
        await self._send_ir_code(self._open_code)
        
        # 模拟开启过程
        self._attr_is_opening = True
        self._attr_is_closing = False
        self.async_write_ha_state()
        
        # 计算开启时间：根据当前位置到0%的距离
        open_time = (self._attr_current_cover_position / 100) * self._close_time
        
        self._movement_task = asyncio.create_task(
            self._simulate_movement(0, open_time)
        )

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        if self._movement_task:
            self._movement_task.cancel()
            
        _LOGGER.info(f"Closing curtain {self.name} with code: {self._close_code}")
        
        # 这里可以添加发送红外码的逻辑
        await self._send_ir_code(self._close_code)
        
        # 模拟关闭过程
        self._attr_is_closing = True
        self._attr_is_opening = False
        self.async_write_ha_state()
        
        # 计算关闭时间：根据当前位置到100%的距离
        close_time = ((100 - self._attr_current_cover_position) / 100) * self._close_time
        
        self._movement_task = asyncio.create_task(
            self._simulate_movement(100, close_time)
        )

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover."""
        if self._movement_task:
            self._movement_task.cancel()
            self._movement_task = None
            
        _LOGGER.info(f"Stopping curtain {self.name} with code: {self._pause_code}")
        
        # 发送暂停码
        await self._send_ir_code(self._pause_code)
        
        self._attr_is_opening = False
        self._attr_is_closing = False
        self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Move the cover to a specific position."""
        position = kwargs[ATTR_POSITION]
        
        if self._movement_task:
            self._movement_task.cancel()
            
        current_pos = self._attr_current_cover_position
        target_pos = position
        
        if target_pos > current_pos:
            # 需要关闭更多
            _LOGGER.info(f"Closing curtain {self.name} to {target_pos}%")
            await self._send_ir_code(self._close_code)
            self._attr_is_closing = True
            self._attr_is_opening = False
        elif target_pos < current_pos:
            # 需要开启更多
            _LOGGER.info(f"Opening curtain {self.name} to {target_pos}%")
            await self._send_ir_code(self._open_code)
            self._attr_is_opening = True
            self._attr_is_closing = False
        else:
            return
            
        self.async_write_ha_state()
        
        # 计算移动时间
        distance = abs(target_pos - current_pos)
        move_time = (distance / 100) * self._close_time
        
        self._movement_task = asyncio.create_task(
            self._simulate_movement(target_pos, move_time)
        )

    async def _send_ir_code(self, code: str) -> None:
        """发送红外码到Broadlink设备."""
        try:
            # 尝试通过Broadlink服务发送红外码
            if self._broadlink_device:
                service_data = {
                    "entity_id": f"remote.{self._broadlink_device}",
                    "command": code
                }
                
                await self._hass.services.async_call(
                    "remote", "send_command", service_data, blocking=True
                )
                _LOGGER.info("Sent IR code via Broadlink: %s", code)
            else:
                # 如果没有配置Broadlink设备，记录日志
                _LOGGER.warning("No Broadlink device configured, simulating IR code: %s", code)
                await asyncio.sleep(0.5)
                
        except Exception as e:
            _LOGGER.error("Failed to send IR code via Broadlink: %s", e)
            # 回退到模拟模式
            _LOGGER.debug("Falling back to simulation for IR code: %s", code)
            await asyncio.sleep(0.5)

    async def _simulate_movement(self, target_position: int, duration: float) -> None:
        """模拟窗帘移动过程."""
        if duration <= 0:
            return
            
        steps = max(10, int(duration * 2))  # 每0.5秒更新一次
        step_duration = duration / steps
        step_size = (target_position - self._attr_current_cover_position) / steps
        
        try:
            for _ in range(steps):
                await asyncio.sleep(step_duration)
                self._attr_current_cover_position += step_size
                self._attr_current_cover_position = max(0, min(100, self._attr_current_cover_position))
                
                # 更新状态
                self._attr_is_closed = self._attr_current_cover_position >= 99
                self.async_write_ha_state()
                
            # 移动完成
            self._attr_current_cover_position = target_position
            self._attr_is_opening = False
            self._attr_is_closing = False
            self._attr_is_closed = self._attr_current_cover_position >= 99
            self.async_write_ha_state()
            
        except asyncio.CancelledError:
            # 移动被中断
            _LOGGER.debug(f"Curtain movement cancelled at {self._attr_current_cover_position}%")
            self._attr_is_opening = False
            self._attr_is_closing = False
            self.async_write_ha_state()