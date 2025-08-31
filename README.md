# Boardlink Curtain Control

一个用于Home Assistant的HACS自定义组件，用于控制通过红外信号控制的窗帘。

## 功能特性

- 🎯 支持开、关、暂停三个基本操作
- 📊 精确的位置控制（0%完全开启，100%完全关闭）
- ⏱️ 可配置的关闭时间，用于准确计算位置
- 🎮 支持Home Assistant的标准窗帘卡片
- 📱 完全集成到Home Assistant的移动应用和Web界面

## 安装

### 通过HACS安装（推荐）

1. 打开HACS
2. 点击"集成"
3. 点击右下角的"+"号
4. 搜索"Boardlink Curtain Control"
5. 点击安装

### 手动安装

1. 下载`boardlink_curtain`文件夹
2. 将其复制到`config/custom_components/`目录下
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

### 在Lovelace界面中使用

添加一个实体卡片或窗帘卡片，选择你配置的窗帘实体即可。

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