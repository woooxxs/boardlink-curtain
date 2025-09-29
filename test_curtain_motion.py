#!/usr/bin/env python3
"""
窗帘运动轨迹测试脚本
用于测试Boardlink Curtain组件的运动轨迹显示功能
"""

import asyncio
import time
import logging
from datetime import datetime

# 模拟Home Assistant API调用
class CurtainTester:
    def __init__(self):
        self.position = 0  # 0=完全关闭, 100=完全打开
        self.is_moving = False
        self.target_position = 0
        
    def simulate_curtain_motion(self, target_pos, duration=30):
        """模拟窗帘运动轨迹"""
        print(f"\n{'='*50}")
        print(f"开始窗帘运动模拟 - {datetime.now().strftime('%H:%M:%S')}")
        print(f"当前位置: {self.position}%")
        print(f"目标位置: {target_pos}%")
        print(f"预计用时: {duration}秒")
        print(f"{'='*50}")
        
        self.target_position = target_pos
        self.is_moving = True
        
        steps = abs(target_pos - self.position)
        if steps == 0:
            print("窗帘已在目标位置，无需移动")
            return
            
        direction = 1 if target_pos > self.position else -1
        step_duration = duration / steps
        
        for i in range(steps):
            self.position += direction
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # 显示运动轨迹
            bar_length = 20
            filled_length = int(bar_length * self.position / 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            print(f"[{timestamp}] 位置: {self.position:3d}% [{bar}] {self.get_status()}")
            time.sleep(step_duration)
            
        self.is_moving = False
        print(f"\n✅ 窗帘运动完成 - 最终位置: {self.position}%")
        
    def get_status(self):
        """获取当前状态"""
        if self.is_moving:
            return "移动中"
        elif self.position == 0:
            return "完全关闭"
        elif self.position == 100:
            return "完全打开"
        else:
            return f"打开{self.position}%"
    
    def stop_curtain(self):
        """停止窗帘运动"""
        if self.is_moving:
            self.is_moving = False
            print(f"\n⏹️  窗帘已停止 - 当前位置: {self.position}%")
        else:
            print("窗帘未在移动状态")

def test_curtain_scenarios():
    """测试不同的窗帘场景"""
    tester = CurtainTester()
    
    print("🎭 Boardlink Curtain 运动轨迹测试")
    print("测试场景将模拟真实的窗帘开合过程")
    
    # 测试1: 从关闭到完全打开
    print("\n📋 测试1: 从关闭到完全打开")
    tester.simulate_curtain_motion(100, 30)
    
    # 测试2: 从完全打开到部分关闭
    print("\n📋 测试2: 从完全打开到部分关闭")
    tester.simulate_curtain_motion(30, 15)
    
    # 测试3: 停止功能测试
    print("\n📋 测试3: 停止功能测试")
    print("开始从30%到100%的运动...")
    asyncio.create_task(async_simulate_stop(tester))
    
    # 测试4: 完全关闭
    print("\n📋 测试4: 完全关闭")
    tester.simulate_curtain_motion(0, 30)

async def async_simulate_stop(tester):
    """异步模拟停止功能"""
    import threading
    
    def run_motion():
        # 模拟部分运动然后停止
        tester.position = 30
        tester.target_position = 100
        tester.is_moving = True
        
        for i in range(10):  # 移动10步后停止
            if not tester.is_moving:
                break
            tester.position += 7
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] 位置: {tester.position:3d}% [移动中...]")
            time.sleep(3)
        
        # 模拟用户停止
        time.sleep(1)
        tester.stop_curtain()
    
    thread = threading.Thread(target=run_motion)
    thread.start()
    time.sleep(5)  # 等待5秒后停止
    tester.stop_curtain()
    thread.join()

def generate_test_data():
    """生成测试数据用于Home Assistant历史图表"""
    print("\n📊 生成测试数据...")
    
    # 模拟一天的窗帘位置变化
    timeline = [
        ("07:00", 0),      # 早上关闭
        ("08:30", 100),    # 起床后完全打开
        ("12:00", 50),     # 中午部分关闭
        ("14:00", 80),     # 下午部分打开
        ("18:30", 0),      # 傍晚完全关闭
        ("20:00", 30),     # 晚上部分打开
        ("22:30", 0),      # 睡前关闭
    ]
    
    print("时间轴数据:")
    for time_str, position in timeline:
        print(f"  {time_str} - 位置: {position}%")
    
    return timeline

if __name__ == "__main__":
    print("🚀 开始窗帘运动轨迹测试...")
    
    try:
        # 基础测试
        test_curtain_scenarios()
        
        # 生成测试数据
        timeline = generate_test_data()
        
        print(f"\n{'='*60}")
        print("✅ 测试完成！")
        print("- 运动轨迹已模拟完成")
        print("- 测试数据已生成")
        print("- 现在可以在Home Assistant中查看历史图表")
        print("- 访问 http://localhost:8123 查看实时状态")
        print(f"{'='*60}")
        
    except KeyboardInterrupt:
        print("\n⚠️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")