#!/usr/bin/env python3
"""
Boardlink Curtain 设置验证脚本
验证Docker环境和组件配置
"""

import os
import subprocess
import sys
from pathlib import Path

def check_docker():
    """检查Docker环境"""
    print("🔍 检查Docker环境...")
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker版本: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker未安装或未运行")
            return False
    except FileNotFoundError:
        print("❌ Docker未安装")
        return False

def check_docker_compose():
    """检查Docker Compose"""
    print("🔍 检查Docker Compose...")
    try:
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose版本: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker Compose不可用")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose未安装")
        return False

def check_config_files():
    """检查配置文件"""
    print("🔍 检查配置文件...")
    
    required_files = [
        'docker-compose.yml',
        'test_config/configuration.yaml',
        'custom_components/boardlink_curtain/__init__.py',
        'custom_components/boardlink_curtain/cover.py',
        'custom_components/boardlink_curtain/config_flow.py',
        'custom_components/boardlink_curtain/manifest.json'
    ]
    
    all_exists = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 缺失")
            all_exists = False
    
    return all_exists

def check_directory_structure():
    """检查目录结构"""
    print("🔍 检查目录结构...")
    
    required_dirs = [
        'custom_components',
        'custom_components/boardlink_curtain',
        'custom_components/boardlink_curtain/translations',
        'test_config',
        'test_config/.storage'
    ]
    
    all_exists = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"✅ {directory}/ 存在")
        else:
            print(f"❌ {directory}/ 缺失")
            all_exists = False
    
    return all_exists

def check_port_availability():
    """检查端口可用性"""
    print("🔍 检查端口8123...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', 8123))
        sock.close()
        
        if result == 0:
            print("❌ 端口8123已被占用")
            return False
        else:
            print("✅ 端口8123可用")
            return True
    except Exception as e:
        print(f"⚠️  端口检查失败: {e}")
        return True

def validate_configuration():
    """验证配置文件语法"""
    print("🔍 验证配置文件语法...")
    
    config_file = 'test_config/configuration.yaml'
    if not os.path.exists(config_file):
        print("❌ 配置文件不存在")
        return False
    
    try:
        # 简单的YAML语法检查
        with open(config_file, 'r') as f:
            content = f.read()
            
        # 检查基本结构
        if 'homeassistant:' in content and 'boardlink_curtain:' in content:
            print("✅ 配置文件语法基本正确")
            return True
        else:
            print("❌ 配置文件缺少必要部分")
            return False
            
    except Exception as e:
        print(f"❌ 配置文件读取失败: {e}")
        return False

def main():
    """主验证函数"""
    print("🚀 Boardlink Curtain 设置验证")
    print("=" * 50)
    
    # 切换到脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 工作目录: {os.getcwd()}")
    
    # 执行检查
    checks = [
        check_docker(),
        check_docker_compose(),
        check_config_files(),
        check_directory_structure(),
        check_port_availability(),
        validate_configuration()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks):
        print("🎉 所有检查通过！环境准备就绪")
        print("\n📋 下一步操作:")
        print("1. 启动测试环境: ./quick_test.sh")
        print("2. 或手动启动: docker-compose up -d")
        print("3. 访问: http://localhost:8123")
        print("4. 添加Boardlink Curtain集成")
        return True
    else:
        print("❌ 部分检查未通过，请修复问题")
        print("\n🔧 常见问题解决:")
        print("- 安装Docker: https://docs.docker.com/get-docker/")
        print("- 检查端口占用: lsof -i :8123")
        print("- 验证配置文件语法")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)