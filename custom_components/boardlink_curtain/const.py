"""Constants for the Boardlink Curtain integration."""

DOMAIN = "boardlink_curtain"

CONF_OPEN_CODE = "open_code"
CONF_CLOSE_CODE = "close_code"
CONF_PAUSE_CODE = "pause_code"
CONF_CLOSE_TIME = "close_time"
CONF_BROADLINK_DEVICE = "broadlink_device"
CONF_BROADLINK_TYPE = "broadlink_type"

DEFAULT_CLOSE_TIME = 30

# 窗帘状态
CURTAIN_OPEN = 0  # 完全开启 0%
CURTAIN_CLOSE = 100  # 完全关闭 100%

# Broadlink设备类型
BROADLINK_TYPES = [
    "RM2",
    "RM3",
    "RM4",
    "RM4C",
    "RM4_MINI",
    "RM4_PRO",
    "RM_MINI3"
]