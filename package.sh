#!/bin/bash

# Boardlink Curtain Control 打包脚本
# 用于创建HACS可用的压缩包

set -e

echo "🚀 开始打包 Boardlink Curtain Control..."

# 创建临时目录
TEMP_DIR=$(mktemp -d)
PACKAGE_NAME="boardlink_curtain"
VERSION="1.0.0"
ZIP_NAME="${PACKAGE_NAME}-${VERSION}.zip"

echo "📁 创建临时目录: $TEMP_DIR"

# 复制必要的文件到临时目录
cp -r custom_components/boardlink_curtain "$TEMP_DIR/"
cp README.md "$TEMP_DIR/"
cp info.md "$TEMP_DIR/"
cp hacs.json "$TEMP_DIR/"
cp lovelace_examples.md "$TEMP_DIR/"

# 进入临时目录
cd "$TEMP_DIR"

# 创建压缩包
zip -r "$ZIP_NAME" . -x "*.DS_Store" "*.git*" "__pycache__" "*.pyc"

# 移动到项目根目录
mv "$ZIP_NAME" ../

echo "✅ 打包完成！"
echo "📦 生成的文件: $ZIP_NAME"
echo "📊 文件大小: $(du -h "../$ZIP_NAME" | cut -f1)"

# 清理临时目录
# rm -rf "$TEMP_DIR"

echo "🧹 清理完成"