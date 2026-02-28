# CLI 参考 - Claude Code

**来源**: https://code.claude.com/docs/zh-CN/cli-reference

> Claude Code 命令行界面参考，包括命令、标志和配置选项。

---

## 目录

- [CLI 命令](#cli-命令)
- [CLI 标志](#cli-标志)
- [Agents 标志格式](#agents-标志格式)
- [系统提示标志](#系统提示标志)

---

## CLI 命令

您可以使用这些命令启动会话、管道内容、恢复对话和管理更新：

| 命令 | 描述 | 示例 |
|------|------|------|
| claude | 启动交互式会话 | claude |
| claude "query" | 使用初始提示启动交互式会话 | claude "explain this project" |
| claude -p "query" | 通过 SDK 查询，然后退出 | claude -p "explain this function" |
| cat file \| claude -p "query" | 处理管道内容 | cat logs.txt \| claude -p "explain" |
| claude -c | 继续当前目录中最近的对话 | claude -c |
| claude -c -p "query" | 通过 SDK 继续 | claude -c -p "Check for type errors" |
| claude -r " \<session\>" "query" | 按 ID 或名称恢复会话 | claude -r "auth-refactor" "Finish this PR" |
| claude update | 更新到最新版本 | claude update |
| claude auth login | 登录您的 Anthropic 账户 | claude auth login --email user@example.com --sso |
| claude auth logout | 从您的 Anthropic 账户登出 | claude auth logout |
| claude auth status | 显示身份验证状态 | claude auth status |
| claude agents | 列出所有已配置的 subagents | claude agents |
| claude mcp | 配置 MCP 服务器 | 请参阅 MCP 文档 |
| claude remote-control | 启动 Remote Control 会话 | claude remote-control |

---

## CLI 标志

使用这些命令行标志自定义 Claude Code 的行为：

| 标志 | 描述 | 示例 |
|------|------|------|
| --add-dir | 添加额外的工作目录供 Claude 访问 | claude --add-dir ../apps ../lib |
| --agent | 为当前会话指定代理 | claude --agent my-custom-agent |
| --agents | 通过 JSON 动态定义自定义 subagents | claude --agents '{"reviewer":{...}}' |
| --allow-dangerously-skip-permissions | 启用权限绕过选项 | claude --permission-mode plan --allow-dangerously-skip-permissions |
| --allowedTools | 无需提示权限即可执行的工具 | "Bash(git log *)" "Read" |
| --append-system-prompt | 附加自定义文本到系统提示 | claude --append-system-prompt "Always use TypeScript" |
| --append-system-prompt-file | 从文件加载额外的系统提示 | claude -p --append-system-prompt-file ./extra-rules.txt |
| --betas | 包含 Beta 标头 | claude --betas interleaved-thinking |
| --chrome | 启用 Chrome 浏览器集成 | claude --chrome |
| --continue, -c | 加载当前目录中最近的对话 | claude --continue |
| --dangerously-skip-permissions | 跳过所有权限提示 | claude --dangerously-skip-permissions |
| --debug | 启用调试模式 | claude --debug "api,hooks" |
| --disable-slash-commands | 禁用所有 skills 和 slash commands | claude --disable-slash-commands |
| --disallowedTools | 从模型上下文中删除的工具 | "Bash(git log *)" "Edit" |
| --fallback-model | 默认模型过载时的回退模型 | claude -p --fallback-model sonnet |
| --fork-session | 恢复时创建新的会话 ID | claude --resume abc123 --fork-session |
| --from-pr | 恢复链接到 GitHub PR 的会话 | claude --from-pr 123 |
| --ide | 启动时自动连接到 IDE | claude --ide |
| --init | 运行初始化 hooks 并启动交互模式 | claude --init |
| --init-only | 运行初始化 hooks 并退出 | claude --init-only |
| --include-partial-messages | 包含部分流事件 | claude -p --output-format stream-json --include-partial-messages |
| --input-format | 指定打印模式输入格式 | claude -p --output-format json --input-format stream-json |
| --json-schema | 获得与 JSON Schema 匹配的验证 JSON | claude -p --json-schema '{...}' |
| --maintenance | 运行维护 hooks 并退出 | claude --maintenance |
| --max-budget-usd | API 调用前停止的最大金额 | claude -p --max-budget-usd 5.00 |
| --max-turns | 限制代理轮数 | claude -p --max-turns 3 |
| --mcp-config | 加载 MCP 服务器配置 | claude --mcp-config ./mcp.json |
| --model | 为当前会话设置模型 | claude --model claude-sonnet-4-6 |
| --no-chrome | 禁用 Chrome 浏览器集成 | claude --no-chrome |
| --no-session-persistence | 禁用会话持久化 | claude -p --no-session-persistence |
| --output-format | 指定打印模式输出格式 | claude -p "query" --output-format json |
| --permission-mode | 以指定的权限模式开始 | claude --permission-mode plan |
| --permission-prompt-tool | 指定 MCP 工具处理权限提示 | claude -p --permission-prompt-tool mcp_auth_tool |
| --plugin-dir | 仅为此会话加载 plugins | claude --plugin-dir ./my-plugins |
| --print, -p | 打印响应而不进入交互模式 | claude -p "query" |
| --remote | 在 claude.ai 上创建网络会话 | claude --remote "Fix the login bug" |
| --resume, -r | 恢复特定会话 | claude --resume auth-refactor |
| --session-id | 使用特定的会话 ID | claude --session-id "uuid" |
| --setting-sources | 加载的设置源 | claude --setting-sources user,project |
| --settings | 设置 JSON 文件路径 | claude --settings ./settings.json |
| --strict-mcp-config | 仅使用 --mcp-config 中的 MCP | claude --strict-mcp-config --mcp-config ./mcp.json |
| --system-prompt | 替换整个系统提示 | claude --system-prompt "You are a Python expert" |
| --system-prompt-file | 从文件加载系统提示 | claude -p --system-prompt-file ./custom-prompt.txt |
| --teleport | 恢复网络会话 | claude --teleport |
| --teammate-mode | 设置 agent team 队友显示方式 | claude --teammate-mode in-process |
| --tools | 限制 Claude 可以使用的内置工具 | claude --tools "Bash,Edit,Read" |
| --verbose | 启用详细日志记录 | claude --verbose |
| --version, -v | 输出版本号 | claude -v |
| --worktree, -w | 在隔离的 git worktree 中启动 | claude -w feature-auth |

---

## Agents 标志格式

`--agents` 标志接受一个 JSON 对象，定义一个或多个自定义 subagents。

### 必需字段

| 字段 | 描述 |
|------|------|
| description | 何时应调用 subagent 的自然语言描述 |
| prompt | 指导 subagent 行为的系统提示 |

### 可选字段

| 字段 | 描述 |
|------|------|
| tools | subagent 可以使用的工具数组 |
| disallowedTools | 明确拒绝的工具名称数组 |
| model | 要使用的模型别名：sonnet、opus、haiku 或 inherit |
| skills | 预加载到 subagent 上下文中的 skill 名称数组 |
| mcpServers | 此 subagent 的 MCP servers 数组 |
| maxTurns | subagent 停止前的最大代理轮数 |

### 示例

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

---

## 系统提示标志

Claude Code 提供四个标志用于自定义系统提示：

| 标志 | 行为 | 模式 | 用例 |
|------|------|------|------|
| --system-prompt | 替换整个默认提示 | 交互 + 打印 | 完全控制 Claude 的行为 |
| --system-prompt-file | 替换为文件内容 | 仅打印 | 从文件加载提示 |
| --append-system-prompt | 附加到默认提示 | 交互 + 打印 | 添加特定指令 |
| --append-system-prompt-file | 附加文件内容到默认提示 | 仅打印 | 从文件加载额外指令 |

### 使用场景

**--system-prompt**: 当您需要完全控制 Claude 的系统提示时使用
```bash
claude --system-prompt "You are a Python expert who only writes type-annotated code"
```

**--system-prompt-file**: 当您想从文件加载自定义提示时使用
```bash
claude -p --system-prompt-file ./prompts/code-review.txt "Review this PR"
```

**--append-system-prompt**: 当您想添加特定指令同时保持 Claude Code 的默认功能完整时使用
```bash
claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
```

**--append-system-prompt-file**: 当您想从文件附加指令同时保持 Claude Code 的默认值时使用
```bash
claude -p --append-system-prompt-file ./prompts/style-rules.txt "Review this PR"
```

### 注意事项

- `--system-prompt` 和 `--system-prompt-file` 互斥
- 附加标志可以与任一替换标志一起使用
- 建议使用 `--append-system-prompt` 或 `--append-system-prompt-file`，因为它们保留 Claude Code 的内置功能

---

## 相关链接

- [Chrome 扩展](https://code.claude.com/docs/zh-CN/chrome) - 浏览器自动化和网络测试
- [交互模式](https://code.claude.com/docs/zh-CN/interactive-mode) - 快捷键、输入模式和交互功能
- [快速入门指南](https://code.claude.com/docs/zh-CN/quickstart) - Claude Code 入门
- [常见工作流](https://code.claude.com/docs/zh-CN/best-practices) - 高级工作流和模式
- [设置](https://code.claude.com/docs/zh-CN/settings) - 配置选项
