#!/bin/bash

# Boardlink Curtain 测试环境启动脚本 - 带运动轨迹显示
# 一键启动Home Assistant并配置窗帘控制面板

set -e

echo "🚀 启动Boardlink Curtain测试环境..."
echo "========================================"

# 颜色输出函数
red() { echo -e "\033[31m$1\033[0m"; }
green() { echo -e "\033[32m$1\033[0m"; }
yellow() { echo -e "\033[33m$1\033[0m"; }
blue() { echo -e "\033[34m$1\033[0m"; }

# 检查Docker环境
echo "📋 检查环境..."
if ! command -v docker &> /dev/null; then
    red "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    red "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 清理旧容器
echo "🧹 清理旧容器..."
docker-compose down --remove-orphans 2>/dev/null || true

# 检查端口占用
echo "🔍 检查端口8123..."
if lsof -i :8123 &> /dev/null; then
    yellow "⚠️  端口8123被占用，正在终止占用进程..."
    lsof -ti :8123 | xargs kill -9 2>/dev/null || true
fi

# 确保配置文件存在
echo "📁 检查配置文件..."
if [ ! -f "test_config/configuration.yaml" ]; then
    red "❌ 配置文件不存在，请检查test_config目录"
    exit 1
fi

# 启动服务
echo "🐳 启动Home Assistant容器..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
for i in {1..30}; do
    if curl -s http://localhost:8123 &> /dev/null; then
        green "✅ Home Assistant已成功启动!"
        break
    fi
    if [ $i -eq 30 ]; then
        red "❌ 服务启动超时，请检查日志"
        docker-compose logs homeassistant
        exit 1
    fi
    echo -n "."
    sleep 2
done

# 显示状态
echo ""
echo "🎯 服务状态:"
docker-compose ps

# 显示访问信息
echo ""
echo "========================================"
green "🎉 测试环境启动成功!"
echo "========================================"
echo ""
blue "🔗 访问地址:"
echo "   • Home Assistant: http://localhost:8123"
echo "   • 首次访问需要创建管理员账户"
echo ""
blue "🎛️  窗帘控制面板:"
echo "   • 实体ID: cover.test_curtain"
echo "   • 红外码配置: send_open / send_close / send_stop"
echo ""
blue "📊 运动轨迹查看:"
echo "   • 实时位置: 仪表盘 -> 窗帘控制中心"
echo "   • 历史轨迹: 开发者工具 -> 统计"
echo ""

# 提供快捷命令
echo "🔧 快捷命令:"
echo "   查看日志:    docker-compose logs -f homeassistant"
echo "   重启服务:    docker-compose restart"
echo "   停止服务:    docker-compose down"
echo "   清理数据:    rm -rf test_config/.storage/*"
echo ""

# 启动监控
echo "📊 启动监控..."
python3 test_curtain_motion.py &

# 提供下一步操作提示
echo ""
yellow "📋 下一步操作:"
echo "1. 打开浏览器访问 http://localhost:8123"
echo "2. 创建管理员账户并完成初始化"
echo "3. 在配置 -> 设备与服务中添加 'Boardlink Curtain'"
echo "4. 在仪表盘 -> 窗帘控制中心查看运动轨迹"
echo ""

# 可选：打开浏览器
if command -v open &> /dev/null; then
    echo "🌐 正在打开浏览器..."
    sleep 3
    open http://localhost:8123
elif command -v xdg-open &> /dev/null; then
    echo "🌐 正在打开浏览器..."
    sleep 3
    xdg-open http://localhost:8123
fi

echo ""
green "🎊 一切就绪！开始测试Boardlink Curtain吧！"