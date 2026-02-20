# Claude Code Hooks 事件参考

> 基于官方文档和 everything-claude-code 实际验证

## 有效的 Hook 事件

| 事件 | 触发时机 |
|------|----------|
| `PreToolUse` | 工具执行**前** |
| `PostToolUse` | 工具执行**后** |
| `SessionStart` | 会话开始 |
| `SessionEnd` | 会话结束 |
| `PreCompact` | 上下文压缩**前** |

## 常见错误

- ❌ `ToolUseStart` - 无效事件名称
- ✅ `PostToolUse` - 正确

## 配置结构

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'before tool'",
            "async": false
          }
        ]
      }
    ]
  }
}
```

## matcher 匹配规则

- `*` - 匹配所有
- `Bash` - 匹配 Bash 工具
- `Write|Edit` - 匹配 Write 或 Edit 工具
- `startup|resume` - 匹配特定会话事件
