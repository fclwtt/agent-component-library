# Gateway

消息网关，包含消息路由、平台适配（Telegram、Discord、微信等）、会话管理、消息投递

## 组件信息

- **ID**: `gateway`
- **分类**: infrastructure
- **版本**: 1.0.0
- **模块数**: 65

## 实现

### Hermes

- **来源**: NousResearch/hermes-agent
- **Commit**: `503867864`

## 模块列表

- `gateway\__init__.py`
- `gateway\authz_mixin.py`
- `gateway\builtin_hooks\__init__.py`
- `gateway\channel_directory.py`
- `gateway\code_skew.py`
- `gateway\config.py`
- `gateway\delivery.py`
- `gateway\display_config.py`
- `gateway\drain_control.py`
- `gateway\hooks.py`
- `gateway\kanban_watchers.py`
- `gateway\memory_monitor.py`
- `gateway\message_timestamps.py`
- `gateway\mirror.py`
- `gateway\pairing.py`
- `gateway\platform_registry.py`
- `gateway\platforms\__init__.py`
- `gateway\platforms\_http_client_limits.py`
- `gateway\platforms\api_server.py`
- `gateway\platforms\base.py`
- ... 还有 45 个模块

## 接口

### 提供

（待定义）

### 依赖

（待定义）

## 使用示例

（待补充）