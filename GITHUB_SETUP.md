# GitHub仓库设置指南

## 🚀 一键添加到HACS设置步骤

### 1. 创建GitHub仓库

1. 登录GitHub
2. 创建新仓库：`boardlink-curtain`
3. 将当前项目文件上传到仓库

### 2. 文件结构确认

确保仓库根目录包含：
```
boardlink-curtain/
├── custom_components/
│   └── boardlink_curtain/
│       ├── __init__.py
│       ├── manifest.json
│       ├── config_flow.py
│       ├── const.py
│       ├── cover.py
│       └── translations/
├── .github/
│   └── workflows/
│       ├── validate.yml
│       └── release.yml
├── hacs.json
├── README.md
├── info.md
├── logo.png
└── logo.svg
```

### 3. 修改配置文件

更新以下文件中的GitHub用户名：
- `manifest.json`中的`documentation`和`issue_tracker`
- `README.md`中的所有GitHub链接

### 4. 发布版本

1. 在GitHub仓库点击"Releases"
2. 点击"Create a new release"
3. 创建标签如`v1.0.0`
4. 发布版本

### 5. 添加到HACS商店

用户现在可以通过以下方式安装：

#### 方法1：一键按钮（推荐）
点击README中的"添加到HACS"按钮

#### 方法2：手动添加仓库
1. 打开HACS → 集成 → 自定义仓库
2. 添加：`https://github.com/你的用户名/boardlink-curtain`
3. 类别选择：Integration
4. 安装"Boardlink Curtain Control"

## 📋 一键安装按钮代码

```markdown
[![添加到HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=你的用户名&repository=boardlink-curtain&category=integration)
```

## ✅ 验证检查清单

- [ ] 所有文件已上传到GitHub
- [ ] manifest.json中的链接已更新
- [ ] README.md中的徽章已更新
- [ ] 已创建GitHub Release
- [ ] 通过HACS验证工作流
- [ ] 一键安装按钮可正常工作