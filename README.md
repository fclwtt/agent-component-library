# Agent Component Library

AI Agent组件库，包含从多个开源Agent框架拆解出的标准化组件。

## 目录结构

```
agent-component-library/
├── index.yaml              # 总索引
├── components/             # 组件库（按功能组织）
│   └── {功能名}/
│       ├── component.yaml          # 通用接口描述
│       ├── hermes/                 # Hermes实现
│       │   ├── implementation.yaml
│       │   └── modules/
│       └── openclaw/               # OpenClaw实现（未来）
├── interfaces/             # 接口协议库
│   ├── memory-provider.yaml
│   ├── tool-registry.yaml
│   └── ...
├── frameworks/             # 框架组装方案
│   ├── hermes/
│   │   └── framework.yaml
│   └── magic-orange-b1/    # 我们自己的组合
└── adapters/               # 适配层（混合架构改造）
```

## 当前状态

- ✅ Hermes框架已拆解（44个组件，152个源码文件）
- 🔄 目录结构已调整为支持多框架
- ⏳ OpenClaw待拆解
- ⏳ 通用接口标准待提炼
- ⏳ 混合架构改造待实施

## 组件统计

| 类型 | 数量 |
|------|------|
| 核心引擎 | 8 |
| 工具 | 23 |
| 网关 | 5 |
| 基础设施 | 7 |
| 执行环境 | 1 |
| **总计** | **44** |

## 接口定义

- MemoryProvider（记忆提供者）
- ToolRegistry（工具注册表）
- PlatformRegistry（平台注册表）
- ProviderProfile（模型提供者）
- LLMCalling（LLM调用）
- ContextManagement（上下文管理）

## 项目目标

1. 拆解多个开源Agent框架（Hermes、OpenClaw、CrewAI等）
2. 提炼通用接口标准
3. 实现混合架构改造
4. 支持按需组装不同场景的Agent应用

## License

MIT
