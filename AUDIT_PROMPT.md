# Agent Component Library - 第三方审查任务

审查依据文件：`AUDIT_PROMPT.md`（本文件）
审查报告输出：`THIRD_PARTY_REVIEW.md`（请写入仓库根目录）

## 任务

审查 https://github.com/fclwtt/agent-component-library 仓库的组件隔离改造工作。

## ⚠️ 重要：勿参考旧审计报告

`audit/_archive/` 目录中存档的是早期（v1/v2）审计报告，数据已过时。请忽略这些文件，基于当前代码独立审查。

## 项目背景

该仓库是一个 AI Agent 组件库，从 Hermes Agent 框架拆解出 15 个标准化组件。改造的核心思路：

1. **不是所有组件都必须独立。** 6 个 Core 组件（state-management、infrastructure、entry-points、llm-client、tool-system、agent-engine）构成系统底座，允许它们之间有受控耦合。Core 组件的 modules/ 路径全局可用，彼此可直接引用。

2. **9 个 Optional 组件（cli、tui、gateway、plugin-system、skill-system、cron、memory-system、security、acp-adapter）必须完全独立。** 每个 Optional 组件自身带有运行所需的全部代码副本，不依赖其他 Optional 组件的模块。

3. **每个组件通过 api.py 暴露公共接口**，其他组件通过 `from hermes.{name}.api import X` 调用。

## 仓库结构

```
agent-component-library/
└── hermes/
    ├── __init__.py            ← Python 包入口
    ├── tool-system/api.py     ← 15 个组件，每个有 api.py + modules/
    ├── agent-engine/api.py
    ├── ... 
    ├── spec/interfaces/       ← 接口契约 YAML
    ├── tests/                 ← 测试
    └── audit/_archive/        ← ⚠️ 已过时，勿参考
```

## 审查维度

### 1. 结构合理性
目录层级是否清晰？组件划分是否合理？README 与实际结构是否一致？

### 2. 组件独立性
6 个 Core 组件之间的耦合是否受控？9 个 Optional 组件是否确实不依赖其他 Optional 组件？移除一个 Optional 组件后其他组件是否仍能正常工作？

### 3. 接口设计
api.py 是否提供清晰的 Protocol 和工厂函数？component.yaml 的接口声明是否完整？

### 4. 测试与质量
测试是否覆盖关键功能？是否能可靠验证组件独立性？代码风格是否一致？

### 5. 构建与部署
pip install 是否可用？构建、测试、推送流程是否可重复？

## 输出要求

审查结论写入 `THIRD_PARTY_REVIEW.md`，包含：
- 每个维度的评估结论（通过 / 需改进 / 不通过）
- 具体的发现和建议
- 最重要的 3 个问题（无论正面负面）
- 总体评估
