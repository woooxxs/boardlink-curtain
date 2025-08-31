# Boardlink Curtain Control

一个用于Home Assistant的HACS自定义组件，用于控制通过红外信号控制的窗帘。

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/woooxxs/boardlink-curtain?style=for-the-badge)](https://github.com/woooxxs/boardlink-curtain/releases)
[![License](https://img.shields.io/github/license/woooxxs/boardlink-curtain?style=for-the-badge)](LICENSE)

## 功能特性

- 🎯 支持开、关、暂停三个基本操作
- 📊 精确的位置控制（0%完全开启，100%完全关闭）
- ⏱️ 可配置的关闭时间，用于准确计算位置
- 🎮 支持Home Assistant的标准窗帘卡片
- 📱 完全集成到Home Assistant的移动应用和Web界面
- 🔴 **Broadlink集成**：支持通过Broadlink设备发送真实红外码

## 安装

### 一键添加到HACS（推荐）

[![添加到HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=woooxxs&repository=boardlink-curtain&category=integration)

点击上方按钮直接添加到HACS，或按照以下步骤手动添加：

### 通过HACS安装

1. 打开HACS → 集成 → 自定义仓库
2. 添加仓库地址：`https://github.com/woooxxs/boardlink-curtain`
3. 搜索"Boardlink Curtain Control"并安装

### 手动安装

1. 下载[最新版本](https://github.com/woooxxs/boardlink-curtain/releases/latest)
2. 解压后将`custom_components/boardlink_curtain`文件夹复制到`config/custom_components/`目录下
3. 重启Home Assistant

## 配置

安装后，在Home Assistant的配置->设备与服务->添加集成中搜索"Boardlink Curtain Control"进行配置。

### 配置参数

- **名称**: 窗帘的名称，将显示在界面上
- **开启红外码**: 发送给窗帘的开启信号代码
- **关闭红外码**: 发送给窗帘的关闭信号代码
- **暂停红外码**: 发送给窗帘的暂停信号代码
- **关闭时间**: 窗帘从完全开启到完全关闭所需的时间（秒）

## 使用方法

### 1. 配置窗帘
1. 进入 **配置** → **设备与服务** → **添加集成**
2. 搜索 **Boardlink Curtain Control**
3. 填写配置信息：
   - **窗帘名称**：给您的窗帘起个名字
   - **开启红外码**：填入开启窗帘的红外码
   - **关闭红外码**：填入关闭窗帘的红外码
   - **暂停红外码**：填入暂停窗帘的红外码
   - **完全关闭时间**：窗帘从完全打开到完全关闭所需的时间（秒）
   - **Broadlink设备**：选择您的Broadlink设备（可选）
   - **Broadlink设备类型**：选择正确的设备型号

### 2. 配置Broadlink（可选）
要使用真实的红外码发送功能，请参见 [Broadlink配置指南](BROADLINK_SETUP.md)

### 3. 添加到界面
1. 进入 **配置** → **仪表板**
2. 编辑您的Lovelace界面
3. 添加 **实体卡片** 或 **窗帘卡片**
4. 选择您创建的窗帘实体

示例YAML配置：

```yaml
type: entities
entities:
  - cover.living_room_curtain
title: 客厅窗帘
```

或者使用窗帘卡片：

```yaml
type: cover
entity: cover.living_room_curtain
```

### 自动化示例

```yaml
automation:
  - alias: "晚上自动关窗帘"
    trigger:
      platform: sun
      event: sunset
      offset: "00:30:00"
    action:
      service: cover.close_cover
      target:
        entity_id: cover.living_room_curtain

  - alias: "早上自动开窗帘"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      service: cover.open_cover
      target:
        entity_id: cover.bedroom_curtain
```

## 红外码获取

要获取窗帘的红外码，你可以：

1. 使用Broadlink RM设备学习原始红外码
2. 使用其他红外学习设备
3. 从窗帘的遥控器获取

## 故障排除

### 常见问题

1. **窗帘不响应**：检查红外码是否正确
2. **位置不准确**：调整关闭时间参数
3. **设备不显示**：确认组件已正确安装并重启Home Assistant

### 调试日志

在`configuration.yaml`中添加以下配置以启用调试日志：

```yaml
logger:
  logs:
    custom_components.boardlink_curtain: debug
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License