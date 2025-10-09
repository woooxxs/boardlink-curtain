"""Support for Boardlink curtain."""
import asyncio
import logging
import time
from typing import Any, Final

from homeassistant.components.cover import (
    ATTR_POSITION,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_CLOSE_CODE,
    CONF_CLOSE_TIME,
    CONF_OPEN_CODE,
    CONF_PAUSE_CODE,
    DEFAULT_CLOSE_TIME,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# 窗帘状态常量
CURTAIN_OPEN: Final = 100  # 完全开启 100%
CURTAIN_CLOSE: Final = 0  # 完全关闭 0%


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Boardlink curtain from a config entry."""
    # 从配置项获取配置数据
    config = hass.data[DOMAIN][entry.entry_id]
    
    # 创建窗帘实体
    curtain = BoardlinkCurtain(
        config,
        entry.entry_id,
    )
    
    async_add_entities([curtain])


class BoardlinkCurtain(CoverEntity):
    """Representation of a Boardlink curtain."""
    
    _attr_should_poll = False
    _attr_supported_features = (
        CoverEntityFeature.OPEN
        | CoverEntityFeature.CLOSE
        | CoverEntityFeature.SET_POSITION
        | CoverEntityFeature.STOP
    )

    def __init__(
        self,
        config: dict[str, Any],
        entry_id: str,
    ) -> None:
        """Initialize the curtain."""
        self._config = config
        self._entry_id = entry_id
        
        # 从配置中获取参数
        self._open_code = config.get(CONF_OPEN_CODE)
        self._close_code = config.get(CONF_CLOSE_CODE)
        self._pause_code = config.get(CONF_PAUSE_CODE)
        self._close_time = config.get(CONF_CLOSE_TIME, DEFAULT_CLOSE_TIME)
        
        # 实体属性
        self._attr_name = config.get("name", "Boardlink Curtain")
        self._attr_unique_id = entry_id
        
        # 状态属性
        self._attr_current_cover_position = CURTAIN_OPEN
        self._attr_is_closed = False
        self._last_operation_start_time = None
        self._expected_end_time = None
        self._target_position = None
        
        # 逐步更新位置的属性
        self._update_position_task = None
        self._is_moving = False

    async def _send_ir_code(self, code: str) -> None:
        """Send IR code to the curtain."""
        if code:
            _LOGGER.info("Sending IR code for curtain %s: %s", self._attr_name, code)
            # 使用模拟脚本服务发送红外指令
            try:
                # 调用script.mock_send_ir服务发送红外指令
                await self.hass.services.async_call(
                    "script",
                    "mock_send_ir",
                    {
                        "code": code
                    },
                    blocking=False
                )
                _LOGGER.info("Successfully sent IR code: %s", code)
            except Exception as e:
                _LOGGER.error("Failed to send IR code %s: %s", code, str(e))
        else:
            _LOGGER.warning("No IR code configured for curtain %s", self._attr_name)

    async def async_open_cover(self, **kwargs: Any) -> None:
        """Open the curtain."""
        _LOGGER.info("Opening curtain %s with code: %s", self._attr_name, self._open_code)
        
        # 发送开启指令
        await self._send_ir_code(self._open_code)
        
        # 记录开始时间和目标时间
        self._last_operation_start_time = time.time()
        self._target_position = CURTAIN_OPEN
        
        # 计算运行时间
        current_position = self._attr_current_cover_position
        if current_position != CURTAIN_OPEN:
            # 计算需要运行的时间（秒）
            position_diff = abs(CURTAIN_OPEN - current_position)
            run_time = (position_diff / 100.0) * self._close_time
            self._expected_end_time = self._last_operation_start_time + run_time
            _LOGGER.info("Curtain %s will run for %.1f seconds to reach fully open position", self._attr_name, run_time)
        
        # 更新状态
        self._attr_current_cover_position = CURTAIN_OPEN
        self._attr_is_closed = False
        self.async_write_ha_state()
        
        _LOGGER.info("Curtain %s is now fully open (position: %d%%)", self._attr_name, CURTAIN_OPEN)

    async def async_close_cover(self, **kwargs: Any) -> None:
        """Close the curtain."""
        _LOGGER.info("Closing curtain %s with code: %s", self._attr_name, self._close_code)
        
        # 发送关闭指令
        await self._send_ir_code(self._close_code)
        
        # 记录开始时间和目标时间
        self._last_operation_start_time = time.time()
        self._target_position = CURTAIN_CLOSE
        
        # 计算运行时间
        current_position = self._attr_current_cover_position
        if current_position != CURTAIN_CLOSE:
            # 计算需要运行的时间（秒）
            position_diff = abs(CURTAIN_CLOSE - current_position)
            run_time = (position_diff / 100.0) * self._close_time
            self._expected_end_time = self._last_operation_start_time + run_time
            _LOGGER.info("Curtain %s will run for %.1f seconds to reach fully closed position", self._attr_name, run_time)
        
        # 更新状态
        self._attr_current_cover_position = CURTAIN_CLOSE
        self._attr_is_closed = True
        self.async_write_ha_state()
        
        _LOGGER.info("Curtain %s is now fully closed (position: %d%%)", self._attr_name, CURTAIN_CLOSE)

    async def _update_position_during_movement(self, start_position: int, target_position: int, run_time: float) -> None:
        """在窗帘移动过程中逐步更新位置值。"""
        try:
            _LOGGER.info("Starting position update from %d%% to %d%% over %.1f seconds", 
                        start_position, target_position, run_time)
            
            # 计算每秒位置变化
            position_diff = target_position - start_position
            start_time = time.time()
            
            # 每0.5秒更新一次位置
            update_interval = 0.5
            steps = int(run_time / update_interval)
            
            if steps <= 0:
                steps = 1
                
            position_step = position_diff / steps
            
            for i in range(steps):
                # 检查是否被取消
                if not self._is_moving:
                    break
                    
                # 等待更新间隔
                await asyncio.sleep(update_interval)
                
                # 计算新位置
                elapsed_time = time.time() - start_time
                if elapsed_time >= run_time:
                    new_position = target_position
                else:
                    # 根据时间计算位置
                    progress = elapsed_time / run_time
                    new_position = int(start_position + position_diff * progress)
                
                # 确保位置在有效范围内
                new_position = max(0, min(100, new_position))
                
                # 更新位置
                self._attr_current_cover_position = new_position
                self._attr_is_closed = new_position == CURTAIN_CLOSE
                self.async_write_ha_state()
                
                _LOGGER.info("Curtain %s position updated to: %d%% (step %d/%d)", 
                            self._attr_name, new_position, i+1, steps)
                
                # 如果已达到目标位置，退出循环
                if new_position == target_position:
                    break
                    
            # 确保最终位置正确
            self._attr_current_cover_position = target_position
            self._attr_is_closed = target_position == CURTAIN_CLOSE
            self.async_write_ha_state()
            
            # 清理状态
            self._is_moving = False
            self._update_position_task = None
            
            _LOGGER.info("Curtain %s finished moving to target position: %d%%", 
                        self._attr_name, target_position)
                        
        except asyncio.CancelledError:
            _LOGGER.info("Position update task for curtain %s was cancelled", self._attr_name)
            self._is_moving = False
            self._update_position_task = None
        except Exception as e:
            _LOGGER.error("Error updating position for curtain %s: %s", self._attr_name, str(e))
            self._is_moving = False
            self._update_position_task = None

    async def async_stop_cover(self, **kwargs: Any) -> None:
        """Stop the curtain."""
        _LOGGER.info("Stopping curtain %s with code: %s", self._attr_name, self._pause_code)
        
        # 发送暂停指令
        await self._send_ir_code(self._pause_code)
        
        # 停止位置更新任务
        if self._update_position_task:
            self._update_position_task.cancel()
            try:
                await self._update_position_task
            except asyncio.CancelledError:
                pass
            self._update_position_task = None
            
        # 记录停止时的位置
        current_position = self._attr_current_cover_position
        _LOGGER.info("Curtain %s stopped at position: %d%%", self._attr_name, current_position)
        
        # 清除操作计时器
        self._last_operation_start_time = None
        self._expected_end_time = None
        self._target_position = None
        self._is_moving = False
        
        # 状态保持不变，仅停止动作
        self.async_write_ha_state()

    async def async_set_cover_position(self, **kwargs: Any) -> None:
        """Move the curtain to a specific position."""
        position = kwargs[ATTR_POSITION]
        _LOGGER.info("Setting curtain %s position to: %d%%", self._attr_name, position)
        
        # 如果正在移动，先取消之前的任务
        if self._update_position_task:
            self._update_position_task.cancel()
            try:
                await self._update_position_task
            except asyncio.CancelledError:
                pass
            self._update_position_task = None
            
        # 记录目标位置
        self._target_position = position
        self._is_moving = True
        
        # 根据位置发送相应的指令
        if position == CURTAIN_OPEN:
            # 发送开启指令
            await self._send_ir_code(self._open_code)
            # 记录开始时间和目标时间
            self._last_operation_start_time = time.time()
            # 计算运行时间
            current_position = self._attr_current_cover_position
            if current_position != position:
                # 计算需要运行的时间（秒）
                position_diff = abs(position - current_position)
                run_time = (position_diff / 100.0) * self._close_time
                self._expected_end_time = self._last_operation_start_time + run_time
                _LOGGER.info("Curtain %s will run for %.1f seconds to reach position %d%%", self._attr_name, run_time, position)
                # 启动位置更新任务
                self._update_position_task = self.hass.async_create_task(self._update_position_during_movement(current_position, position, run_time))
        elif position == CURTAIN_CLOSE:
            # 发送关闭指令
            await self._send_ir_code(self._close_code)
            # 记录开始时间和目标时间
            self._last_operation_start_time = time.time()
            # 计算运行时间
            current_position = self._attr_current_cover_position
            if current_position != position:
                # 计算需要运行的时间（秒）
                position_diff = abs(position - current_position)
                run_time = (position_diff / 100.0) * self._close_time
                self._expected_end_time = self._last_operation_start_time + run_time
                _LOGGER.info("Curtain %s will run for %.1f seconds to reach position %d%%", self._attr_name, run_time, position)
                # 启动位置更新任务
                self._update_position_task = self.hass.async_create_task(self._update_position_during_movement(current_position, position, run_time))
        else:
            # 对于中间位置，需要特殊的处理方式
            _LOGGER.info("Setting curtain %s to intermediate position: %d%%", self._attr_name, position)
            # 计算需要运行的时间（秒）
            current_position = self._attr_current_cover_position
            position_diff = abs(position - current_position)
            run_time = (position_diff / 100.0) * self._close_time
            
            # 确定运行方向
            if position > current_position:
                # 需要开启窗帘
                await self._send_ir_code(self._open_code)
                _LOGGER.info("Opening curtain %s to reach position %d%%", self._attr_name, position)
            else:
                # 需要关闭窗帘
                await self._send_ir_code(self._close_code)
                _LOGGER.info("Closing curtain %s to reach position %d%%", self._attr_name, position)
                
            # 记录开始时间和目标时间
            self._last_operation_start_time = time.time()
            self._expected_end_time = self._last_operation_start_time + run_time
            
            _LOGGER.info("Curtain %s will run for %.1f seconds to reach intermediate position %d%%", self._attr_name, run_time, position)
            
            # 启动位置更新任务
            self._update_position_task = self.hass.async_create_task(self._update_position_during_movement(current_position, position, run_time))
            
            # 调度停止操作
            if run_time > 0:
                # 使用异步延迟来调度停止操作
                async def _scheduled_stop():
                    await asyncio.sleep(run_time)
                    await self.async_stop_cover()
                    _LOGGER.info("Curtain %s reached target position: %d%%", self._attr_name, position)
                
                # 启动异步任务
                self.hass.async_create_task(_scheduled_stop())
                
        # 更新状态（对于完全开启和完全关闭的情况，或者作为中间位置的初始状态）
        # 注意：在逐步更新模式下，位置会在_update_position_during_movement中更新
        if not self._update_position_task:
            self._attr_current_cover_position = position
            self._attr_is_closed = position == CURTAIN_CLOSE
            self.async_write_ha_state()
            _LOGGER.info("Curtain %s target position set to: %d%%", self._attr_name, position)