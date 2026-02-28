# Hooks 参考 - Claude Code

**来源**: https://code.claude.com/docs/zh-CN/hooks

> Hooks 是用户定义的 shell 命令、HTTP 端点或 LLM 提示，在 Claude Code 生命周期中的特定点自动执行。

---

## 目录

- [Hook 生命周期](#hook-生命周期)
- [Hook 如何解析](#hook-如何解析)
- [配置](#配置)
- [Hook 输入和输出](#hook-输入和输出)
- [Hook 事件](#hook-事件)
  - [SessionStart](#sessionstart)
  - [UserPromptSubmit](#userpromptsubmit)
  - [PreToolUse](#pretooluse)
  - [PermissionRequest](#permissionrequest)
  - [PostToolUse](#posttooluse)
  - [PostToolUseFailure](#posttoolusefailure)
  - [Notification](#notification)
  - [SubagentStart](#subagentstart)
  - [SubagentStop](#subagentstop)
  - [Stop](#stop)
  - [TeammateIdle](#teammateidle)
  - [TaskCompleted](#taskcompleted)
  - [ConfigChange](#configchange)
  - [WorktreeCreate](#worktreecreate)
  - [WorktreeRemove](#worktreeremove)
  - [PreCompact](#precompact)
  - [SessionEnd](#sessionend)
- [基于提示的 Hooks](#基于提示的-hooks)
- [基于代理的 Hooks](#基于代理的-hooks)
- [在后台运行 Hooks](#在后台运行-hooks)
- [安全考虑](#安全考虑)

---

## Hook 生命周期

Hooks 在 Claude Code 会话期间的特定点触发。当事件触发且匹配器匹配时，Claude Code 会将关于该事件的 JSON 上下文传递给您的 hook 处理程序。

| Event | 触发时机 |
|-------|----------|
| SessionStart | 会话开始或恢复时 |
| UserPromptSubmit | 用户提交提示时 |
| PreToolUse | 工具调用执行前。可以阻止 |
| PermissionRequest | 权限对话框显示时 |
| PostToolUse | 工具调用成功后 |
| PostToolUseFailure | 工具调用失败后 |
| Notification | Claude Code 发送通知时 |
| SubagentStart | subagent 生成时 |
| SubagentStop | subagent 完成时 |
| Stop | Claude 完成响应时 |
| TeammateIdle | agent 团队队友即将空闲时 |
| TaskCompleted | 任务被标记为已完成时 |
| ConfigChange | 配置文件在会话期间更改时 |
| WorktreeCreate | 通过 --worktree 创建 worktree 时 |
| WorktreeRemove | worktree 被移除时 |
| PreCompact | 上下文压缩前 |
| SessionEnd | 会话终止时 |

---

## Hook 如何解析

**示例：阻止破坏性 shell 命令的 PreToolUse hook**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

该脚本从 stdin 读取 JSON 输入，提取命令，如果包含 `rm -rf`，则返回 `permissionDecision` 为 "deny"：

```bash
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

**执行流程**:
1. 事件触发 - PreToolUse 事件触发，Claude Code 将工具输入作为 JSON 通过 stdin 发送到 hook
2. 匹配器检查 - 匹配器 "Bash" 与工具名称匹配，因此 block-rm.sh 运行
3. Hook 处理程序运行 - 脚本从输入中提取命令并返回决定
4. Claude Code 对结果采取行动 - 读取 JSON 决定，阻止工具调用

---

## 配置

### Hook 位置

您定义 hook 的位置决定了其范围：

| 位置 | 范围 | 可共享 |
|------|------|--------|
| ~/.claude/settings.json | 您的所有项目 | 否，本地于您的机器 |
| .claude/settings.json | 单个项目 | 是，可以提交到仓库 |
| .claude/settings.local.json | 单个项目 | 否，gitignored |
| 托管策略设置 | 组织范围 | 是，管理员控制 |
| Plugin hooks/hooks.json | 启用插件时 | 是，与插件捆绑 |
| Skill 或 agent frontmatter | 组件活跃时 | 是，在组件文件中定义 |

### 匹配器模式

`matcher` 字段是一个正则表达式字符串，用于过滤 hooks 何时触发。使用 `*` 来匹配所有出现。

| 事件 | 匹配器过滤的内容 | 示例匹配器值 |
|------|------------------|--------------|
| PreToolUse、PostToolUse、PostToolUseFailure、PermissionRequest | 工具名称 | Bash、Edit\|Write、mcp__.* |
| SessionStart | 会话如何启动 | startup、resume、clear、compact |
| SessionEnd | 会话为何结束 | clear、logout、prompt_input_exit |
| Notification | 通知类型 | permission_prompt、idle_prompt |
| SubagentStart | 代理类型 | Bash、Explore、Plan |
| PreCompact | 触发压缩的内容 | manual、auto |
| ConfigChange | 配置源 | user_settings、project_settings |

### Hook 处理程序字段

有四种类型的 hook 处理程序：

| 类型 | 描述 |
|------|------|
| command | 运行 shell 命令。脚本在 stdin 上接收事件的 JSON 输入 |
| http | 将事件的 JSON 输入作为 HTTP POST 请求发送到 URL |
| prompt | 向 Claude 模型发送提示以进行单轮评估 |
| agent | 生成一个可以使用工具来验证条件的 subagent |

**通用字段**:

| 字段 | 必需 | 描述 |
|------|------|------|
| type | 是 | "command"、"http"、"prompt" 或 "agent" |
| timeout | 否 | 取消前的秒数。默认值：命令 600，提示 30，代理 60 |
| statusMessage | 否 | hook 运行时显示的自定义微调消息 |
| once | 否 | 如果为 true，每个会话仅运行一次 |

### 按路径引用脚本

使用环境变量来引用相对于项目或插件根目录的 hook 脚本：

- `$CLAUDE_PROJECT_DIR`: 项目根目录
- `${CLAUDE_PLUGIN_ROOT}`: 插件的根目录

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Hook 输入和输出

### 通用输入字段

所有 hook 事件都接收这些字段作为 JSON：

| 字段 | 描述 |
|------|------|
| session_id | 当前会话标识符 |
| transcript_path | 对话 JSON 的路径 |
| cwd | 调用 hook 时的当前工作目录 |
| permission_mode | 当前权限模式 |
| hook_event_name | 触发的事件名称 |

### 退出代码输出

| 退出代码 | 描述 |
|----------|------|
| 0 | 成功。解析 stdout 以查找 JSON 输出 |
| 2 | 阻止错误。stderr 文本被反馈给 Claude 作为错误消息 |
| 其他 | 非阻止错误。stderr 在详细模式中显示 |

### JSON 输出字段

| 字段 | 默认 | 描述 |
|------|------|------|
| continue | true | 如果为 false，Claude 在 hook 运行后完全停止处理 |
| stopReason | 无 | hook 运行后向用户显示的消息 |
| suppressOutput | false | 如果为 true，从详细模式输出中隐藏 stdout |
| systemMessage | 无 | 向用户显示的警告消息 |

### 决定控制

| 事件 | 决定模式 | 关键字段 |
|------|----------|----------|
| UserPromptSubmit、PostToolUse、PostToolUseFailure、Stop、SubagentStop、ConfigChange | 顶级 decision | decision: "block"、reason |
| TeammateIdle、TaskCompleted | 仅退出代码 | 退出代码 2 阻止操作 |
| PreToolUse | hookSpecificOutput | permissionDecision（allow/deny/ask） |
| PermissionRequest | hookSpecificOutput | decision.behavior（allow/deny） |

---

## Hook 事件

### SessionStart

在 Claude Code 启动新会话或恢复现有会话时运行。

**输入**:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

**匹配器值**:
| 值 | 何时触发 |
|----|----------|
| startup | 新会话 |
| resume | --resume、--continue 或 /resume |
| clear | /clear |
| compact | 自动或手动压缩 |

**决定控制**:
- `additionalContext`: 添加到 Claude 上下文的字符串

**持久化环境变量**:
SessionStart hooks 可以访问 `CLAUDE_ENV_FILE` 环境变量来持久化环境变量。

---

### UserPromptSubmit

在用户提交提示时运行，在 Claude 处理它之前。

**输入**:
```json
{
  "session_id": "abc123",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial"
}
```

**决定控制**:
- `decision`: "block" 防止提示被处理
- `reason`: 当 decision 为 "block" 时向用户显示
- `additionalContext`: 添加到 Claude 上下文的字符串

---

### PreToolUse

在 Claude 创建工具参数后和处理工具调用之前运行。

**输入**:
```json
{
  "session_id": "abc123",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

**工具输入字段**:

**Bash**:
| 字段 | 类型 | 描述 |
|------|------|------|
| command | string | 要执行的 shell 命令 |
| description | string | 命令执行内容的可选描述 |
| timeout | number | 可选超时（毫秒） |
| run_in_background | boolean | 是否在后台运行命令 |

**Write**:
| 字段 | 类型 | 描述 |
|------|------|------|
| file_path | string | 要写入的文件的绝对路径 |
| content | string | 要写入文件的内容 |

**Edit**:
| 字段 | 类型 | 描述 |
|------|------|------|
| file_path | string | 要编辑的文件的绝对路径 |
| old_string | string | 要查找和替换的文本 |
| new_string | string | 替换文本 |
| replace_all | boolean | 是否替换所有出现 |

**决定控制**:
- `permissionDecision`: "allow"、"deny" 或 "ask"
- `permissionDecisionReason`: 向用户显示的原因
- `updatedInput`: 在执行前修改工具的输入参数
- `additionalContext`: 在工具执行前添加到 Claude 上下文的字符串

---

### PermissionRequest

在向用户显示权限对话框时运行。

**输入**:
```json
{
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules"
  },
  "permission_suggestions": [
    { "type": "toolAlwaysAllow", "tool": "Bash" }
  ]
}
```

**决定控制**:
- `decision.behavior`: "allow" 或 "deny"
- `updatedInput`: 仅对 "allow"
- `updatedPermissions`: 仅对 "allow"
- `message`: 仅对 "deny"

---

### PostToolUse

在工具成功完成后立即运行。

**输入**:
```json
{
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  }
}
```

**决定控制**:
- `decision`: "block" 提示 Claude 使用 reason
- `reason`: 当 decision 为 "block" 时向 Claude 显示
- `additionalContext`: Claude 要考虑的其他上下文
- `updatedMCPToolOutput`: 仅对 MCP 工具

---

### PostToolUseFailure

在工具执行失败时运行。

**输入**:
```json
{
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  },
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

---

### Notification

在 Claude Code 发送通知时运行。

**匹配器值**:
| 值 | 描述 |
|----|------|
| permission_prompt | 需要权限批准 |
| idle_prompt | Claude 空闲 |
| auth_success | 认证成功 |
| elicitation_dialog | 征求意见对话框 |

---

### SubagentStart

在通过 Task 工具生成 Claude Code subagent 时运行。

**输入**:
```json
{
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

---

### SubagentStop

在 Claude Code subagent 完成响应时运行。

**输入**:
```json
{
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "path/to/subagent/transcript.jsonl",
  "last_assistant_message": "Analysis complete..."
}
```

---

### Stop

在主 Claude Code 代理完成响应时运行。

**输入**:
```json
{
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring..."
}
```

**决定控制**:
- `decision`: "block" 防止 Claude 停止
- `reason`: 当 decision 为 "block" 时需要

---

### TeammateIdle

在 agent 团队队友在完成其轮次后即将空闲时运行。

**输入**:
```json
{
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

**注意**: 仅使用退出代码，不使用 JSON 决定控制

---

### TaskCompleted

在任务被标记为已完成时运行。

**输入**:
```json
{
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

**注意**: 仅使用退出代码，不使用 JSON 决定控制

---

### ConfigChange

在会话期间配置文件更改时运行。

**匹配器值**:
| 值 | 何时触发 |
|----|----------|
| user_settings | ~/.claude/settings.json 更改 |
| project_settings | .claude/settings.json 更改 |
| local_settings | .claude/settings.local.json 更改 |
| policy_settings | 托管策略设置更改 |
| skills | .claude/skills/ 中的 skill 文件更改 |

**决定控制**:
- `decision`: "block" 防止配置更改被应用
- `reason`: 当 decision 为 "block" 时向用户显示

**注意**: policy_settings 更改无法被阻止

---

### WorktreeCreate

当您运行 `claude --worktree` 时，创建隔离的工作副本。

**输入**:
```json
{
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

**输出**: hook 必须在 stdout 上打印创建的 worktree 目录的绝对路径

---

### WorktreeRemove

worktree 被移除时触发。

**输入**:
```json
{
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/path/to/worktree"
}
```

---

### PreCompact

在 Claude Code 即将运行压缩操作之前运行。

**匹配器值**:
| 值 | 何时触发 |
|----|----------|
| manual | /compact |
| auto | 当上下文窗口满时自动压缩 |

**输入**:
```json
{
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

---

### SessionEnd

在 Claude Code 会话结束时运行。

**原因**:
| 原因 | 描述 |
|------|------|
| clear | 会话使用 /clear 命令清除 |
| logout | 用户登出 |
| prompt_input_exit | 用户在提示输入可见时退出 |
| bypass_permissions_disabled | 绕过权限模式被禁用 |
| other | 其他退出原因 |

---

## 基于提示的 Hooks

除了 Bash 命令 hooks，Claude Code 还支持基于提示的 hooks（type: "prompt"），使用 LLM 来评估是否允许或阻止操作。

**配置**:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**响应架构**:
```json
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

---

## 基于代理的 Hooks

基于代理的 hooks（type: "agent"）生成一个可以使用 Read、Grep 和 Glob 等工具来验证条件的 subagent。

**配置**:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

**特点**:
- subagent 可以使用工具来调查
- 最多 50 轮
- 返回结构化的 { "ok": true/false } 决定

---

## 在后台运行 Hooks

默认情况下，hooks 阻止 Claude 的执行。设置 `"async": true` 以在后台运行 hook。

**配置**:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

**限制**:
- 仅 type: "command" hooks 支持 async
- 异步 hooks 无法阻止工具调用
- Hook 输出在下一个对话轮次上传递

---

## 安全考虑

### 免责声明

命令 hooks 以您的系统用户的完整权限运行。

### 安全最佳实践

- 验证和清理输入：永远不要盲目信任输入数据
- 始终引用 shell 变量：使用 "$VAR" 而不是 $VAR
- 阻止路径遍历：检查文件路径中的 ..
- 使用绝对路径：为脚本指定完整路径
- 跳过敏感文件：避免 .env、.git/、密钥等

---

## 调试 Hooks

运行 `claude --debug` 以查看 hook 执行详细信息。

```
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0
```
