#!/usr/bin/env python3
"""
Boardlink Curtain 集成测试脚本
用于测试自定义组件的功能
"""

import asyncio
import sys
from pathlib import Path

# 添加自定义组件路径
custom_components_path = Path(__file__).parent / 'custom_components'
sys.path.insert(0, str(custom_components_path))

try:
    from homeassistant.core import HomeAssistant
    from homeassistant.setup import async_setup_component
    from custom_components.boardlink_curtain.cover import BoardlinkCurtain
    from custom_components.boardlink_curtain.const import DOMAIN
    print("✅ Home Assistant 组件导入成功")
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保在Home Assistant环境中运行此脚本")
    sys.exit(1)

async def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    # 创建测试配置
    config = {
        DOMAIN: [{
            'name': '测试窗帘',
            'open_code': 'test_open_code',
            'close_code': 'test_close_code',
            'pause_code': 'test_pause_code',
            'close_time': 30
        }]
    }
    
    # 创建Home Assistant实例
    hass = HomeAssistant()
    
    try:
        # 设置组件
        result = await async_setup_component(hass, DOMAIN, config)
        if not result:
            print("❌ 组件设置失败")
            return False
        
        print("✅ 组件设置成功")
        
        # 获取实体
        entities = hass.data[DOMAIN]
        if not entities:
            print("❌ 未找到实体")
            return False
        
        curtain = entities[0]
        print(f"✅ 找到实体: {curtain.name}")
        
        # 测试属性
        print(f"  当前状态: {curtain.state}")
        
        # 测试打开
        print("\n🔧 测试打开窗帘...")
        await curtain.async_open_cover()
        print(f"  打开后状态: {curtain.state}")
        
        # 测试关闭
        print("\n🔧 测试关闭窗帘...")
        await curtain.async_close_cover()
        print(f"  关闭后状态: {curtain.state}")
        
        # 测试停止
        print("\n🔧 测试停止窗帘...")
        await curtain.async_stop_cover()
        print(f"  停止后状态: {curtain.state}")
        
        print("\n🎉 所有基本功能测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await hass.async_stop()

async def main():
    """主测试函数"""
    print("🚀 开始Boardlink Curtain集成测试")
    print("=" * 50)
    
    # 运行测试
    success = await test_basic_functionality()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 测试通过！组件功能正常")
    else:
        print("❌ 测试失败，请检查组件实现")
    
    return success

if __name__ == "__main__":
    # 运行测试
    success = asyncio.run(main())
    
    # 退出码
    sys.exit(0 if success else 1)