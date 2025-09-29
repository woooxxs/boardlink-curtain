#!/bin/bash

# Boardlink Curtain 测试环境启动脚本
# 作者: AI Assistant
# 功能: 快速启动Home Assistant测试环境

set -e

echo "🚀 启动 Boardlink Curtain 测试环境..."

# 创建测试配置目录
if [ ! -d "test_config" ]; then
    echo "📁 创建测试配置目录..."
    mkdir -p test_config
    
    # 创建基本配置文件
    cat > test_config/configuration.yaml << EOF
# 测试用Home Assistant配置

# 基本配置
homeassistant:
  name: Boardlink Curtain Test
  latitude: 39.9042
  longitude: 116.4074
  elevation: 0
  unit_system: metric
  time_zone: Asia/Shanghai

# 前端配置
frontend:
  themes: !include_dir_merge_named themes

# 日志配置
logger:
  default: warning
  logs:
    custom_components.boardlink_curtain: debug
    homeassistant.components.cover: debug

# 模拟一些测试设备
input_boolean:
  mock_broadlink_device:
    name: Mock Broadlink RM Mini 3
    initial: false

# 模拟脚本
script:
  mock_send_ir:
    sequence:
      - service: system_log.write
        data:
          message: "Mock IR code sent: {{ code }}"
          level: info

# 测试用自动化
automation:
  - alias: "测试窗帘状态变化"
    trigger:
      - platform: state
        entity_id: cover.test_curtain
    action:
      - service: system_log.write
        data:
          message: "Curtain state changed to: {{ trigger.to_state.state }}"
          level: info

EOF

    # 创建secrets文件
    cat > test_config/secrets.yaml << EOF
# 测试用secrets
mock_ir_codes:
  open: "JgBQAAABKpIVEhUSFRIVEhUSFRIV..."
  close: "JgBQAAABKpMVEhUSFRIVEhUSFRIV..."
  pause: "JgBQAAABKpQVEhUSFRIVEhUSFRIV..."
EOF

fi

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "✅ 环境检查通过"

# 启动测试环境
echo "🐳 启动Docker容器..."
docker-compose up -d

echo "⏳ 等待Home Assistant启动..."
sleep 10

echo "🎉 测试环境已启动！"
echo ""
echo "📱 访问地址: http://localhost:8123"
echo "📝 日志查看: docker-compose logs -f homeassistant"
echo "🛑 停止环境: docker-compose down"
echo ""
echo "🔧 测试步骤:"
echo "1. 访问 http://localhost:8123"
echo "2. 进入 配置 → 设备与服务 → 添加集成"
echo "3. 搜索 'Boardlink Curtain Control'"
echo "4. 按提示配置窗帘"
echo "5. 在开发者工具中测试实体"