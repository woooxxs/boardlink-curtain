#!/usr/bin/env python3
"""
Boardlink Curtain 本地测试环境
不依赖Docker，直接运行Python测试
"""

import asyncio
import json
import logging
from pathlib import Path
import sys
import os

# 添加组件路径
sys.path.insert(0, str(Path(__file__).parent / "custom_components"))

from custom_components.boardlink_curtain.cover import BoardlinkCurtain
from custom_components.boardlink_curtain.const import *

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MockHomeAssistant:
    """模拟的Home Assistant实例"""
    
    def __init__(self):
        self.services = MockServiceRegistry()
        self.states = {}
        
    async def services_async_call(self, domain, service, service_data, blocking=False):
        """模拟服务调用"""
        logger.info(f"Mock service call: {domain}.{service} with {service_data}")
        return True

class MockServiceRegistry:
    """模拟的服务注册表"""
    
    async def async_call(self, domain, service, service_data, blocking=False):
        """模拟服务调用"""
        logger.info(f"Mock service call: {domain}.{service} with {service_data}")
        return True

class MockBroadlinkDevice:
    """模拟的Broadlink设备"""
    
    def __init__(self, name):
        self.name = name
        self.ir_codes_sent = []
    
    def send_ir_code(self, code):
        """模拟发送红外码"""
        self.ir_codes_sent.append(code)
        logger.info(f"Mock Broadlink {self.name} sent IR code: {code}")
        return True

async def test_curtain_without_broadlink():
    """测试无Broadlink设备的窗帘"""
    print("\n🧪 测试无Broadlink设备的窗帘...")
    
    hass = MockHomeAssistant()
    curtain = BoardlinkCurtain(
        name="测试窗帘",
        open_code="OPEN123",
        close_code="CLOSE123",
        pause_code="PAUSE123",
        close_time=5,
        broadlink_device=None,
        broadlink_type="RM_MINI3",
        unique_id="test_curtain_1",
        hass=hass
    )
    
    print(f"初始位置: {curtain.current_cover_position}%")
    print(f"是否关闭: {curtain.is_closed}")
    
    # 测试关闭
    print("\n🔽 测试关闭窗帘...")
    await curtain.async_close_cover()
    await asyncio.sleep(2)  # 等待移动完成
    print(f"关闭后位置: {curtain.current_cover_position}%")
    print(f"是否关闭: {curtain.is_closed}")
    
    # 测试开启
    print("\n🔼 测试开启窗帘...")
    await curtain.async_open_cover()
    await asyncio.sleep(2)
    print(f"开启后位置: {curtain.current_cover_position}%")
    print(f"是否关闭: {curtain.is_closed}")
    
    # 测试设置位置
    print("\n⏫ 测试设置到50%位置...")
    await curtain.async_set_cover_position(position=50)
    await asyncio.sleep(1)
    print(f"设置后位置: {curtain.current_cover_position}%")
    
    # 测试暂停
    print("\n⏸️ 测试暂停功能...")
    # 先开始移动
    await curtain.async_close_cover()
    await asyncio.sleep(1)  # 移动中
    await curtain.async_stop_cover()
    await asyncio.sleep(0.5)
    print(f"暂停后位置: {curtain.current_cover_position}%")

async def test_curtain_with_broadlink():
    """测试有Broadlink设备的窗帘"""
    print("\n🧪 测试有Broadlink设备的窗帘...")
    
    hass = MockHomeAssistant()
    curtain = BoardlinkCurtain(
        name="Broadlink窗帘",
        open_code="REAL_OPEN",
        close_code="REAL_CLOSE",
        pause_code="REAL_PAUSE",
        close_time=3,
        broadlink_device="mock_broadlink",
        broadlink_type="RM_MINI3",
        unique_id="test_curtain_2",
        hass=hass
    )
    
    # 测试通过Broadlink发送红外码
    print("\n🔴 测试通过Broadlink发送红外码...")
    await curtain.async_open_cover()
    await asyncio.sleep(1)
    
    await curtain.async_close_cover()
    await asyncio.sleep(1)
    
    await curtain.async_stop_cover()
    await asyncio.sleep(0.5)

async def test_error_handling():
    """测试错误处理"""
    print("\n🧪 测试错误处理...")
    
    hass = MockHomeAssistant()
    curtain = BoardlinkCurtain(
        name="错误测试窗帘",
        open_code="ERROR_CODE",
        close_code="ERROR_CODE",
        pause_code="ERROR_CODE",
        close_time=2,
        broadlink_device="nonexistent_device",
        broadlink_type="RM_MINI3",
        unique_id="test_curtain_3",
        hass=hass
    )
    
    # 测试错误处理（会回退到模拟模式）
    print("\n⚠️ 测试Broadlink设备不存在时的回退...")
    await curtain.async_open_cover()
    await asyncio.sleep(1)

async def run_all_tests():
    """运行所有测试"""
    print("🎯 Boardlink Curtain 测试套件")
    print("=" * 50)
    
    try:
        # 测试1: 无Broadlink设备
        await test_curtain_without_broadlink()
        
        # 测试2: 有Broadlink设备
        await test_curtain_with_broadlink()
        
        # 测试3: 错误处理
        await test_error_handling()
        
        print("\n✅ 所有测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 启动本地测试环境...")
    asyncio.run(run_all_tests())