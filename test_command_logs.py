#!/usr/bin/env python3
"""
测试命令日志输出脚本
用于验证Boardlink Curtain组件的特殊命令日志输出功能
"""

import subprocess
import sys
import time
import os
import re
from datetime import datetime

# 颜色输出函数
def print_color(text, color_code):
    """输出带颜色的文本"""
    print(f"\033[{color_code}m{text}\033[0m")

def print_green(text):
    print_color(text, "32")

def print_red(text):
    print_color(text, "31")

def print_blue(text):
    print_color(text, "34")

def print_yellow(text):
    print_color(text, "33")

def check_docker_status():
    """检查Docker是否正在运行"""
    try:
        subprocess.run(["docker", "ps"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def check_hass_container():
    """检查Home Assistant容器是否正在运行"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=boardlink_hass", "--format", "{{.ID}}"] ,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return len(result.stdout.strip()) > 0
    except Exception:
        return False

def follow_logs():
    """实时跟踪Home Assistant日志"""
    print_blue("\n=== 实时日志输出（按Ctrl+C停止） ===")
    print_yellow("正在等待命令执行的日志...")
    
    # 跟踪Docker容器日志
    try:
        process = subprocess.Popen(
            ["docker", "logs", "-f", "boardlink_hass"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        
        # 特殊命令的正则表达式模式
        patterns = {
            "send_open": re.compile(r"执行测试命令: send_open|窗帘.*接收到打开命令"),
            "send_close": re.compile(r"执行测试命令: send_close|窗帘.*接收到关闭命令"),
            "send_stop": re.compile(r"执行测试命令: send_stop|窗帘.*接收到停止命令")
        }
        
        for line in process.stdout:
            # 检查是否包含特殊命令的日志
            for cmd, pattern in patterns.items():
                if pattern.search(line):
                    # 高亮显示特殊命令的日志
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print_green(f"[{timestamp}] {line.strip()}")
                    break
            else:
                # 普通日志
                if "boardlink_curtain" in line.lower():
                    print_blue(line.strip())
                else:
                    # 仅显示错误和警告
                    if any(level in line for level in ["ERROR", "WARNING", "CRITICAL"]):
                        print_red(line.strip())
    except KeyboardInterrupt:
        print_yellow("\n停止日志跟踪")
    except Exception as e:
        print_red(f"跟踪日志出错: {e}")

def send_command(cmd):
    """发送命令到窗帘"""
    print_blue(f"\n发送命令: {cmd}")
    
    try:
        # 根据命令类型构建服务调用
        if cmd == "open":
            service = "cover.open_cover"
        elif cmd == "close":
            service = "cover.close_cover"
        elif cmd == "stop":
            service = "cover.stop_cover"
        else:
            print_red("未知命令")
            return False
        
        # 使用Home Assistant API调用服务
        # 注意：需要先配置长期访问令牌
        # 构造JSON参数
        json_params = '{"entity_id": "cover.test_curtain"}'
        command = f"docker exec -it boardlink_hass bash -c 'hass-cli --server http://localhost:8123 --token YOUR_LONG_LIVED_TOKEN service call {service} {json_params}'"
        
        # 为了演示，我们不实际执行命令，而是模拟命令发送
        print_yellow("注意：此脚本需要配置Home Assistant的长期访问令牌才能实际发送命令")
        print_green(f"模拟发送命令到Home Assistant: {service}")
        print_green(f"请在Home Assistant界面中手动操作窗帘来查看日志输出")
        
        return True
    except Exception as e:
        print_red(f"发送命令失败: {e}")
        return False

def print_menu():
    """打印菜单"""
    print("\n" + "="*50)
    print("    🎮 Boardlink Curtain 命令测试工具    ")
    print("="*50)
    print("1. 启动实时日志监控")
    print("2. 模拟发送打开命令 (send_open)")
    print("3. 模拟发送关闭命令 (send_close)")
    print("4. 模拟发送停止命令 (send_stop)")
    print("5. 查看窗帘状态")
    print("6. 检查测试环境")
    print("0. 退出")
    print("="*50)

def check_environment():
    """检查测试环境是否就绪"""
    print_blue("\n=== 检查测试环境 ===")
    
    # 检查Docker
    if not check_docker_status():
        print_red("❌ Docker未运行，请启动Docker")
        return False
    else:
        print_green("✅ Docker正在运行")
    
    # 检查Home Assistant容器
    if not check_hass_container():
        print_yellow("⚠️  Home Assistant容器未运行，正在启动...")
        try:
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            print_green("✅ Home Assistant容器已启动")
            time.sleep(10)  # 等待启动
        except Exception as e:
            print_red(f"❌ 启动Home Assistant容器失败: {e}")
            return False
    else:
        print_green("✅ Home Assistant容器正在运行")
    
    # 检查配置文件
    config_path = os.path.join(os.path.dirname(__file__), "test_config", "configuration.yaml")
    if not os.path.exists(config_path):
        print_red(f"❌ 配置文件不存在: {config_path}")
        return False
    else:
        # 检查配置文件中是否包含特殊命令
        with open(config_path, "r") as f:
            content = f.read()
            if "send_open" in content and "send_close" in content and "send_stop" in content:
                print_green("✅ 配置文件中已包含特殊测试命令")
            else:
                print_yellow("⚠️  配置文件中可能未包含特殊测试命令")
    
    print_green("✅ 测试环境检查完成")
    return True

def main():
    """主函数"""
    print("🚀 启动Boardlink Curtain命令日志测试工具")
    
    # 检查环境
    if not check_environment():
        print_red("❌ 测试环境未准备好，退出程序")
        sys.exit(1)
    
    while True:
        print_menu()
        choice = input("请选择操作 [0-6]: ")
        
        if choice == "0":
            print_green("👋 感谢使用，再见！")
            break
        elif choice == "1":
            follow_logs()
        elif choice == "2":
            send_command("open")
        elif choice == "3":
            send_command("close")
        elif choice == "4":
            send_command("stop")
        elif choice == "5":
            print_yellow("请在Home Assistant界面中查看窗帘状态")
        elif choice == "6":
            check_environment()
        else:
            print_red("❌ 无效的选择，请重新输入")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_green("\n👋 用户中断，程序退出")
    except Exception as e:
        print_red(f"\n❌ 程序异常: {e}")
        sys.exit(1)