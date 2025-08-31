# Boardlink Curtain Control

## 🎯 功能特点

- ✅ 支持开、关、暂停三个基本操作
- ✅ 精确的位置控制（0%完全开启，100%完全关闭）
- ✅ 可配置的关闭时间，用于准确计算位置
- ✅ 完全集成到Home Assistant的窗帘系统
- ✅ 支持中文和英文界面
- ✅ 响应式设计，适配手机和桌面

## 📁 项目结构

```
custom_components/boardlink_curtain/
├── __init__.py          # 组件初始化
├── manifest.json        # 组件清单
├── config_flow.py       # 配置流程
├── const.py            # 常量定义
├── cover.py            # 窗帘实体类
└── translations/       # 翻译文件
    ├── zh.json         # 中文翻译
    └── en.json         # 英文翻译
```

## 🚀 快速开始

### 1. 安装

**方法1：HACS安装（推荐）**
1. 打开HACS → 集成 → 自定义仓库
2. 添加本仓库地址
3. 搜索"Boardlink Curtain Control"并安装

**方法2：手动安装**
1. 下载本项目
2. 将`custom_components/boardlink_curtain`文件夹复制到你的Home Assistant的`config/custom_components/`目录下
3. 重启Home Assistant

### 2. 配置

1. 进入Home Assistant的"配置" → "设备与服务" → "添加集成"
2. 搜索"Boardlink Curtain Control"
3. 填写以下信息：
   - **窗帘名称**：如"客厅窗帘"
   - **开启红外码**：窗帘开启的红外代码
   - **关闭红外码**：窗帘关闭的红外代码
   - **暂停红外码**：窗帘暂停的红外代码
   - **完全关闭时间**：窗帘从完全开启到完全关闭所需的时间（秒）

### 3. 使用

配置完成后，窗帘会自动出现在你的实体列表中，实体ID格式为：`cover.[窗帘名称]`。

### 4. Lovelace卡片

在Lovelace界面中添加窗帘卡片：

```yaml
type: cover
entity: cover.客厅窗帘
```

## 🔧 高级配置

### 红外码获取

要获取窗帘的红外码，你可以：
1. 使用Broadlink RM设备学习红外码
2. 使用其他红外学习设备
3. 查阅窗帘遥控器的说明书

### 调试

在`configuration.yaml`中添加：

```yaml
logger:
  logs:
    custom_components.boardlink_curtain: debug
```

## 📱 界面展示

- **状态显示**：显示当前开启百分比
- **位置滑块**：可以拖动到任意位置
- **控制按钮**：开、关、暂停三个按钮
- **实时反馈**：显示"正在开启"、"正在关闭"等状态

## 🤝 支持

如有问题，请在GitHub上提交Issue。