# Agent Component Library - 审查提示词

请对 [fclwtt/agent-component-library](https://github.com/fclwtt/agent-component-library) 仓库的改造工作进行全面审查。

---

## 一、仓库结构审查

确认根目录结构：

```
agent-component-library/
├── hermes/                        ← Hermes 框架组件
│   ├── __init__.py
│   ├── tool-system/               ← 15 个组件，每组件有 api.py
│   ├── agent-engine/
│   ├── cli/
│   ├── cron/
│   ├── entry-points/
│   ├── gateway/
│   ├── infrastructure/
│   ├── llm-client/
│   ├── memory-system/
│   ├── plugin-system/
│   ├── security/
│   ├── skill-system/
│   ├── state-management/
│   ├── tui/
│   ├── spec/interfaces/           ← 接口契约 YAML
│   ├── spec/frameworks/           ← 框架组装
│   ├── audit/
│   ├── tests/
│   └── pyproject.toml
├── magic-orange/                  ← 存根
├── scripts/push_to_github.py
├── Makefile
├── pyproject.toml
├── index.yaml
├── README.md
└── AUDIT_PROMPT.md
```

检查项：
- [ ] 根目录结构与上图一致
- [ ] hermes/__init__.py 存在，含 _COMPONENT_MAP 和 __getattr__
- [ ] 每个组件有 api.py、component.yaml、modules/
- [ ] spec/interfaces/ 下有 6 个 YAML 接口定义

---

## 二、组件独立性审查

### 2.1 跨组件引用扫描

从项目根目录运行：

```python
import ast, os
from pathlib import Path
from collections import defaultdict

H = Path('hermes')
COMPS = sorted([d.name for d in H.iterdir() if d.is_dir()
    and not d.name.startswith(('_','.'))
    and d.name not in ('spec','audit','tests')])

comp_files = {}
for c in COMPS:
    files = set()
    base = H / c / 'modules'
    if base.is_dir():
        for item in base.rglob('*.py'):
            if item.name == '__init__.py': continue
            rel = item.relative_to(base)
            files.add(str(rel.with_suffix('')))
    comp_files[c] = files

STDLIB = {'os','sys','json','re','typing','io','abc','enum',
    'dataclasses','pathlib','functools','itertools','collections',
    'asyncio','logging','hashlib','uuid','datetime','math',
    'textwrap','base64','copy','inspect','warnings','traceback',
    'signal','subprocess','threading','multiprocessing','time',
    'http','urllib','xml','csv','html','string','struct','pickle',
    'shelve','tempfile','shutil','glob','fnmatch','linecache',
    '__future__','ssl','socket'}

found = 0
for src in COMPS:
    for py_file in sorted((H / src).rglob('*.py')):
        if py_file.name in ('api.py', '__init__.py'): continue
        try:
            with open(py_file) as f: tree = ast.parse(f.read())
        except SyntaxError: continue
        for node in ast.walk(tree):
            mods = []
            if isinstance(node, ast.Import):
                for a in node.names: mods.append(a.name)
            elif isinstance(node, ast.ImportFrom) and node.module:
                mods.append(node.module)
            for mod_name in mods:
                mod_path = '/'.join(mod_name.split('.'))
                parts = mod_name.split('.')
                if not parts or parts[0] in STDLIB: continue
                for target in COMPS:
                    if target == src: continue
                    if mod_path in comp_files.get(target, set()) \
                        and mod_path not in comp_files.get(src, set()):
                        found += 1
                        break

print(f'Cross-component imports: {found}')
```

- [ ] 结果为 0
- [ ] 非零则列出具体引用

### 2.2 导入验证

```bash
/opt/homebrew/bin/python3.13 -c "
import sys; sys.path.insert(0, '.')
from hermes import tool_system, agent_engine, cli, cron
from hermes import entry_points, gateway, infrastructure, llm_client
from hermes import memory_system, plugin_system, security, skill_system
from hermes import state_management, acp_adapter, tui
print('All 15 OK')
"
```

- [ ] 15 个组件全部可导入
- [ ] 格式为 from hermes.{name} import ...

---

## 三、测试审查

```bash
/opt/homebrew/bin/python3.13 -m pytest hermes/tests/ -q
/opt/homebrew/bin/python3.13 hermes/tests/lint/check_import_isolation.py hermes
```

- [ ] 全部通过，无 FAILED
- [ ] 隔离检查输出 PASS，语法错误警告可忽略

---

## 四、组件隔离完整性

抽查 3 个组件目录，确认每个 hermes 模块的 import 语句只引用：
1. 标准库
2. 本组件 modules/ 内的其他模块
3. 不引用其他组件的 modules/

```bash
cd hermes
for comp in tool-system agent-engine cli; do
    found=$(grep -r "^from " $comp/modules/ --include="*.py" | grep -v "__future__\|typing\|os\|sys\|json\|re\|io\|abc\|enum\|dataclasses\|pathlib\|functools\|itertools\|collections\|asyncio\|logging\|hashlib\|uuid\|datetime\|math\|textwrap\|base64\|copy\|inspect\|warnings\|signal\|subprocess\|threading\|time\|http\|ssl\|socket" | grep -v "^from $comp" | wc -l)
    echo "$comp: $found cross-module refs"
done
```

- [ ] 3 个组件的 cross-module refs 均为 0

---

## 五、整体评估

| 维度 | 标准 | 结果 |
|------|------|------|
| 结构 | monorepo，15 组件 | □ 通过 □ 不通过 |
| 独立性 | 跨组件引用 = 0 | □ 通过 □ 不通过 |
| 测试 | 全部通过 | □ 通过 □ 不通过 |
| 隔离检查 | 0 违规 | □ 通过 □ 不通过 |
| api.py | 15 个都有 | □ 通过 □ 不通过 |
| Python | 3.13 可用 | □ 通过 □ 不通过 |
| 推送 | make push 可用 | □ 通过 □ 不通过 |

总体结论：□ 通过 □ 需修复
