# Claude Code 插件配置规范

> 本文档基于官方文档和 everything-claude-code 项目的实际验证结果

## 配置文件结构

```
.claude-plugin/
├── plugin.json       # 插件核心配置（必需）
├── marketplace.json # 市场发布配置（发布时必需）
├── README.md         # 插件说明文档
└── PLUGIN_SCHEMA_NOTES.md # 字段约束笔记
```

## plugin.json 必需字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 插件名称 |
| `version` | string | 版本号（如 "1.0.0"）|
| `description` | string | 插件描述 |
| `author` | object | 作者信息 |
| `keywords` | array | 关键词数组 |
| `skills` | array | Skills 路径 |
| `agents` | array | Agents 路径（必需逐个列出文件）|
| `commands` | array | Commands 路径 |

## 字段约束规则

### 数组字段

以下字段**必须始终是数组**：
- `agents`
- `commands`
- `skills`
- `keywords`

即使只有一个条目，也必须使用数组格式。

```json
// ❌ 错误
"agents": "./agents/planner.md"

// ✅ 正确
"agents": ["./agents/planner.md"]
```

### Agents 路径规则

**Agents 必须使用显式文件路径**，不接受目录路径：

```json
// ❌ 错误
"agents": ["./agents/"]

// ✅ 正确
"agents": [
  "./agents/planner.md",
  "./agents/architect.md",
  "./agents/code-reviewer.md"
]
```

### Skills 和 Commands

可以接受目录路径：

```json
// ✅ 正确
"skills": ["./skills/"]
"commands": ["./commands/"]
```

### Hooks 字段

**不要在 plugin.json 中添加 `hooks` 字段！**

原因：Claude Code v2.1+ 会自动加载 `hooks/hooks.json`。如果在 plugin.json 中显式声明，会报重复错误：

```
Duplicate hooks file detected: ./hooks/hooks.json resolves to already-loaded file.
```

## marketplace.json 结构

用于发布到插件市场：

```json
{
  "name": "插件市场名称",
  "owner": {
    "name": "所有者名称",
    "email": "邮箱"
  },
  "metadata": {
    "description": "市场描述"
  },
  "plugins": [
    {
      "name": "插件名称",
      "source": "./",
      "description": "插件描述",
      "author": { "name": "作者" },
      "homepage": "首页 URL",
      "repository": "仓库 URL",
      "license": "MIT",
      "keywords": ["关键词"],
      "category": "分类",
      "tags": ["标签"]
    }
  ]
}
```

## 验证命令

安装前验证配置：

```bash
claude plugin validate .claude-plugin/plugin.json
```

## 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `agents: Invalid input` | Agents 使用了目录路径 | 改为显式文件路径数组 |
| `Duplicate hooks file` | 在 plugin.json 中添加了 hooks | 移除 hooks 字段 |
| `version: Invalid input` | 缺少 version 字段 | 添加 version 字段 |
| `expected array, received string` | 字段值不是数组 | 改为数组格式 |

## 文件路径格式

- 始终使用相对路径：`./agents/planner.md`
- 使用正斜杠 `/`，即使在 Windows 上
- 不要使用绝对路径

## 最小有效示例

```json
{
  "version": "1.0.0",
  "agents": [
    "./agents/planner.md",
    "./agents/code-reviewer.md"
  ],
  "commands": ["./commands/"],
  "skills": ["./skills/"]
}
```

## 相关资源

- 官方文档：https://docs.anthropic.com/en/docs/claude-code/plugins
- 市场配置：https://docs.anthropic.com/en/docs/claude-code/plugin-marketplaces
