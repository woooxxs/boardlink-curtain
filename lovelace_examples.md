# Lovelace 卡片配置示例

## 基础窗帘卡片

```yaml
type: cover
entity: cover.living_room_curtain
name: 客厅窗帘
```

## 实体卡片（显示更多控制选项）

```yaml
type: entities
entities:
  - entity: cover.bedroom_curtain
    name: 卧室窗帘
    secondary_info: last-changed
title: 窗帘控制
```

## 水平堆叠卡片（多个窗帘）

```yaml
type: horizontal-stack
cards:
  - type: cover
    entity: cover.living_room_curtain
    name: 客厅
  - type: cover
    entity: cover.bedroom_curtain
    name: 卧室
  - type: cover
    entity: cover.study_curtain
    name: 书房
```

## 自定义按钮卡片

```yaml
type: custom:button-card
template: curtain_card
entity: cover.living_room_curtain
name: 客厅窗帘
show_icon: true
show_name: true
show_state: true
tap_action:
  action: call-service
  service: cover.toggle
  target:
    entity_id: cover.living_room_curtain
hold_action:
  action: more-info
```

## 网格卡片布局

```yaml
type: grid
cards:
  - type: cover
    entity: cover.living_room_curtain
    name: 客厅窗帘
  - type: cover
    entity: cover.bedroom_curtain
    name: 卧室窗帘
  - type: cover
    entity: cover.kitchen_curtain
    name: 厨房窗帘
columns: 2
square: false
```

## 带场景按钮的卡片

```yaml
type: vertical-stack
cards:
  - type: cover
    entity: cover.living_room_curtain
    name: 客厅窗帘
  - type: horizontal-stack
    cards:
      - type: button
        name: 全开
        tap_action:
          action: call-service
          service: cover.open_cover
          target:
            entity_id: cover.living_room_curtain
      - type: button
        name: 全关
        tap_action:
          action: call-service
          service: cover.close_cover
          target:
            entity_id: cover.living_room_curtain
      - type: button
        name: 暂停
        tap_action:
          action: call-service
          service: cover.stop_cover
          target:
            entity_id: cover.living_room_curtain
```

## 条件显示卡片

```yaml
type: conditional
card:
  type: cover
  entity: cover.living_room_curtain
  name: 客厅窗帘
conditions:
  - entity: cover.living_room_curtain
    state_not: "unavailable"
```