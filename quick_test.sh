#!/bin/bash

# Boardlink Curtain 快速测试脚本
# 解决端口映射和网络问题

set -e

echo "🚀 启动 Boardlink Curtain 测试环境..."

# 检查Docker状态
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

# 停止之前的容器（如果存在）
echo "🧹 清理之前的容器..."
docker-compose down 2>/dev/null || true
docker rm -f ha_boardlink_test 2>/dev/null || true

# 确保配置目录存在
mkdir -p test_config

# 创建或更新配置文件
cat > test_config/configuration.yaml << 'EOF'
# 测试用Home Assistant配置
homeassistant:
  name: Boardlink Curtain Test
  latitude: 39.9042
  longitude: 116.4074
  elevation: 0
  unit_system: metric
  time_zone: Asia/Shanghai

# 基本配置
frontend:
  themes: {}

# 日志配置
logger:
  default: warning
  logs:
    custom_components.boardlink_curtain: debug

# 允许访问
http:
  server_host: 0.0.0.0
  server_port: 8123

# 测试用输入布尔值
input_boolean:
  test_switch:
    name: 测试开关
    initial: false
EOF

# 启动容器
echo "🐳 启动Home Assistant容器..."
docker-compose up -d

# 等待容器启动
echo "⏳ 等待容器启动..."
sleep 15

# 检查容器状态
if docker ps | grep -q ha_boardlink_test; then
    echo "✅ 容器启动成功！"
    echo ""
    echo "🌐 访问地址: http://localhost:8123"
    echo "📱 首次访问可能需要等待1-2分钟初始化"
    echo ""
    echo "🔧 测试步骤:"
    echo "1. 打开浏览器访问 http://localhost:8123"
    echo "2. 创建用户账户（首次访问）"
    echo "3. 进入 配置 → 设备与服务 → 添加集成"
    echo "4. 搜索 'Boardlink Curtain Control'"
    echo "5. 按提示配置窗帘参数"
    echo ""
    echo "📊 查看日志:"
    echo "docker-compose logs -f homeassistant"
    echo ""
    echo "🛑 停止测试:"
    echo "docker-compose down"
else
    echo "❌ 容器启动失败"
    echo "查看错误日志:"
    docker-compose logs
fi