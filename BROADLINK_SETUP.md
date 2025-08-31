# Broadlink 设备配置指南

本文档说明如何将博联(Broadlink)红外设备与Boardlink Curtain组件集成，实现真实的红外码发送功能。

## 前提条件

1. 已安装并配置好Broadlink设备（如RM Mini 3、RM4等）
2. 在Home Assistant中已添加Broadlink集成
3. 已学习窗帘遥控器的红外码

## 配置步骤

### 1. 添加Broadlink集成

在Home Assistant中：
1. 进入 **配置** → **设备与服务** → **添加集成**
2. 搜索并选择 **Broadlink**
3. 按照提示添加您的Broadlink设备

### 2. 学习红外码

使用Broadlink设备学习窗帘遥控器的红外码：
1. 在Home Assistant中，找到您的Broadlink设备
2. 点击设备，选择 **学习指令**
3. 依次学习：
   - 开启指令（Open）
   - 关闭指令（Close）
   - 暂停指令（Pause）
4. 记录学习到的红外码（通常是base64编码的字符串）

### 3. 配置窗帘控制

添加Boardlink Curtain集成时：
1. 进入 **配置** → **设备与服务** → **添加集成**
2. 搜索并选择 **Boardlink Curtain Control**
3. 填写配置信息：
   - **窗帘名称**：给您的窗帘起个名字
   - **开启红外码**：填入学习到的开启指令
   - **关闭红外码**：填入学习到的关闭指令
   - **暂停红外码**：填入学习到的暂停指令
   - **完全关闭时间**：窗帘从完全打开到完全关闭所需的时间（秒）
   - **Broadlink设备**：选择您的Broadlink设备（可选）
   - **Broadlink设备类型**：选择正确的设备型号

## 使用说明

### 通过Broadlink发送红外码

当配置了Broadlink设备后，组件会自动：
1. 通过选定的Broadlink设备发送红外码
2. 实时更新窗帘状态
3. 支持精确位置控制

### 手动模式

如果没有配置Broadlink设备，组件将以模拟模式运行：
- 记录红外码但不实际发送
- 仅模拟窗帘状态变化
- 适用于测试配置

## 故障排除

### Broadlink设备未找到

如果配置时找不到Broadlink设备：
1. 确认Broadlink集成已正确安装
2. 检查设备名称是否正确
3. 重启Home Assistant

### 红外码发送失败

如果红外码发送失败：
1. 检查红外码格式是否正确
2. 确认Broadlink设备与窗帘的距离
3. 检查设备电源和网络连接
4. 查看Home Assistant日志获取详细信息

### 位置不准确

如果窗帘位置显示不准确：
1. 调整"完全关闭时间"设置
2. 确保红外码学习正确
3. 检查Broadlink设备响应时间

## 示例配置

### 配置文件示例

```yaml
# configuration.yaml (可选)
boardlink_curtain:
  - name: "客厅窗帘"
    open_code: "JgBQAAABKpIVEhUSFRIVEhUSFRIV..."
    close_code: "JgBQAAABKpMVEhUSFRIVEhUSFRIV..."
    pause_code: "JgBQAAABKpQVEhUSFRIVEhUSFRIV..."
    close_time: 25
    broadlink_device: "broadlink_rm_mini_3"
    broadlink_type: "RM_MINI3"
```

### Lovelace卡片示例

```yaml
type: entities
entities:
  - cover.客厅窗帘
title: 客厅窗帘控制
```

## 支持的Broadlink设备

- RM2
- RM3
- RM4
- RM4C
- RM4 Mini
- RM4 Pro
- RM Mini 3

## 获取帮助

如需更多帮助：
1. 查看 [Broadlink官方文档](https://www.home-assistant.io/integrations/broadlink/)
2. 检查组件日志
3. 在GitHub上提交问题