# Hooks Guide 官方文档

> 来源: https://code.claude.com/docs/zh-CN/hooks-guide

> 爬取时间: 自动生成

---

- Claude Code 钩子入门 - Claude Code Docs

[跳转到主要内容](#content-area)

[Claude Code Docs home page](/docs)

简体中文

搜索...

⌘K询问AI

搜索...

Navigation

使用 Claude Code 构建

Claude Code 钩子入门

[快速开始

](/docs/zh-CN/overview)[使用 Claude Code 构建

](/docs/zh-CN/sub-agents)[部署

](/docs/zh-CN/third-party-integrations)[管理

](/docs/zh-CN/setup)[配置

](/docs/zh-CN/settings)[参考

](/docs/zh-CN/cli-reference)[资源

](/docs/zh-CN/legal-and-compliance)

##### 使用 Claude Code 构建

[

创建自定义 subagents

](/docs/zh-CN/sub-agents)
- [

协调 Claude Code 会话团队

](/docs/zh-CN/agent-teams)
- [

创建插件

](/docs/zh-CN/plugins)
- [

通过市场发现和安装预构建插件

](/docs/zh-CN/discover-plugins)
- [

使用 skills 扩展 Claude

](/docs/zh-CN/skills)
- [

输出样式

](/docs/zh-CN/output-styles)
- [

Claude Code 钩子入门

](/docs/zh-CN/hooks-guide)
- [

编程使用

](/docs/zh-CN/headless)
- [

Model Context Protocol (MCP)

](/docs/zh-CN/mcp)
- [

故障排除

](/docs/zh-CN/troubleshooting)

在此页面

- [钩子事件概述](#%E9%92%A9%E5%AD%90%E4%BA%8B%E4%BB%B6%E6%A6%82%E8%BF%B0)
- [快速入门](#%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8)
- [前置条件](#%E5%89%8D%E7%BD%AE%E6%9D%A1%E4%BB%B6)
- [步骤 1：打开钩子配置](#%E6%AD%A5%E9%AA%A4-1%EF%BC%9A%E6%89%93%E5%BC%80%E9%92%A9%E5%AD%90%E9%85%8D%E7%BD%AE)
- [步骤 2：添加匹配器](#%E6%AD%A5%E9%AA%A4-2%EF%BC%9A%E6%B7%BB%E5%8A%A0%E5%8C%B9%E9%85%8D%E5%99%A8)
- [步骤 3：添加钩子](#%E6%AD%A5%E9%AA%A4-3%EF%BC%9A%E6%B7%BB%E5%8A%A0%E9%92%A9%E5%AD%90)
- [步骤 4：保存您的配置](#%E6%AD%A5%E9%AA%A4-4%EF%BC%9A%E4%BF%9D%E5%AD%98%E6%82%A8%E7%9A%84%E9%85%8D%E7%BD%AE)
- [步骤 5：验证您的钩子](#%E6%AD%A5%E9%AA%A4-5%EF%BC%9A%E9%AA%8C%E8%AF%81%E6%82%A8%E7%9A%84%E9%92%A9%E5%AD%90)
- [步骤 6：测试您的钩子](#%E6%AD%A5%E9%AA%A4-6%EF%BC%9A%E6%B5%8B%E8%AF%95%E6%82%A8%E7%9A%84%E9%92%A9%E5%AD%90)
- [更多示例](#%E6%9B%B4%E5%A4%9A%E7%A4%BA%E4%BE%8B)
- [代码格式化钩子](#%E4%BB%A3%E7%A0%81%E6%A0%BC%E5%BC%8F%E5%8C%96%E9%92%A9%E5%AD%90)
- [Markdown 格式化钩子](#markdown-%E6%A0%BC%E5%BC%8F%E5%8C%96%E9%92%A9%E5%AD%90)
- [自定义通知钩子](#%E8%87%AA%E5%AE%9A%E4%B9%89%E9%80%9A%E7%9F%A5%E9%92%A9%E5%AD%90)
- [文件保护钩子](#%E6%96%87%E4%BB%B6%E4%BF%9D%E6%8A%A4%E9%92%A9%E5%AD%90)
- [了解更多](#%E4%BA%86%E8%A7%A3%E6%9B%B4%E5%A4%9A)

Claude Code 钩子是用户定义的 shell 命令，在 Claude Code 生命周期的各个点执行。钩子提供对 Claude Code 行为的确定性控制，确保某些操作总是发生，而不是依赖 LLM 选择运行它们。

有关钩子的参考文档，请参阅 [钩子参考](/docs/zh-CN/hooks)。

钩子的示例用例包括：

- **通知**：自定义当 Claude Code 等待您的输入或权限运行某些操作时如何获得通知。

- **自动格式化**：在每次文件编辑后对 .ts 文件运行 `prettier`，对 .go 文件运行 `gofmt` 等。

- **日志记录**：跟踪和计数所有执行的命令以进行合规性或调试。

- **反馈**：当 Claude Code 生成不遵循您的代码库约定的代码时提供自动反馈。

- **自定义权限**：阻止对生产文件或敏感目录的修改。

通过将这些规则编码为钩子而不是提示指令，您将建议转变为应用级代码，每次在预期运行时执行。

在添加钩子时，您必须考虑钩子的安全隐患，因为钩子在代理循环期间使用您当前环境的凭证自动运行。例如，恶意钩子代码可能会泄露您的数据。在注册钩子之前，始终审查您的钩子实现。有关完整的安全最佳实践，请参阅钩子参考文档中的 [安全考虑](/docs/zh-CN/hooks#security-considerations)。

##
[​

](#钩子事件概述)
钩子事件概述

Claude Code 提供了在工作流的不同点运行的多个钩子事件：

- **PreToolUse**：在工具调用之前运行（可以阻止它们）

- **PermissionRequest**：在显示权限对话框时运行（可以允许或拒绝）

- **PostToolUse**：在工具调用完成后运行

- **UserPromptSubmit**：当用户提交提示时运行，在 Claude 处理之前

- **Notification**：当 Claude Code 发送通知时运行

- **Stop**：当 Claude Code 完成响应时运行

- **SubagentStop**：当子代理任务完成时运行

- **PreCompact**：在 Claude Code 即将运行压缩操作之前运行

- **SessionStart**：当 Claude Code 启动新会话或恢复现有会话时运行

- **SessionEnd**：当 Claude Code 会话结束时运行

每个事件接收不同的数据，并可以以不同的方式控制 Claude 的行为。
##
[​

](#快速入门)
快速入门

在本快速入门中，您将添加一个钩子来记录 Claude Code 运行的 shell 命令。
###
[​

](#前置条件)
前置条件

安装 `jq` 用于命令行中的 JSON 处理。
###
[​

](#步骤-1：打开钩子配置)
步骤 1：打开钩子配置

运行 `/hooks` [斜杠命令](/docs/zh-CN/slash-commands) 并选择 `PreToolUse` 钩子事件。
`PreToolUse` 钩子在工具调用之前运行，可以阻止它们，同时向 Claude 提供关于如何不同处理的反馈。
###
[​

](#步骤-2：添加匹配器)
步骤 2：添加匹配器

选择 `+ Add new matcher…` 仅在 Bash 工具调用上运行您的钩子。
为匹配器输入 `Bash`。

您可以使用 `*` 来匹配所有工具。

###
[​

](#步骤-3：添加钩子)
步骤 3：添加钩子

选择 `+ Add new hook…` 并输入此命令：

报告错误代码

复制

询问AI

`jq -r '"\(.tool_input.command) - \(.tool_input.description // "No description")"' >> ~/.claude/bash-command-log.txt
`

###
[​

](#步骤-4：保存您的配置)
步骤 4：保存您的配置

对于存储位置，选择 `User settings`，因为您正在记录到您的主目录。然后此钩子将应用于所有项目，而不仅仅是您的当前项目。
然后按 `Esc` 直到您返回 REPL。您的钩子现在已注册。
###
[​

](#步骤-5：验证您的钩子)
步骤 5：验证您的钩子

再次运行 `/hooks` 或检查 `~/.claude/settings.json` 以查看您的配置：

报告错误代码

复制

询问AI

`{
"hooks": {
"PreToolUse": [
{
"matcher": "Bash",
"hooks": [
{
"type": "command",
"command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"No description\")\"' >> ~/.claude/bash-command-log.txt"
}
]
}
]
}
}
`

###
[​

](#步骤-6：测试您的钩子)
步骤 6：测试您的钩子

要求 Claude 运行一个简单的命令，如 `ls`，并检查您的日志文件：

报告错误代码

复制

询问AI

`cat ~/.claude/bash-command-log.txt
`

您应该看到类似的条目：

报告错误代码

复制

询问AI

`ls - Lists files and directories
`

##
[​

](#更多示例)
更多示例

有关完整的示例实现，请参阅我们公共代码库中的 [bash 命令验证器示例](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)。

###
[​

](#代码格式化钩子)
代码格式化钩子

在编辑后自动格式化 TypeScript 文件：

报告错误代码

复制

询问AI

`{
"hooks": {
"PostToolUse": [
{
"matcher": "Edit|Write",
"hooks": [
{
"type": "command",
"command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.ts$'; then npx prettier --write \"$file_path\"; fi; }"
}
]
}
]
}
}
`

###
[​

](#markdown-格式化钩子)
Markdown 格式化钩子

自动修复 markdown 文件中缺失的语言标签和格式化问题：

报告错误代码

复制

询问AI

`{
"hooks": {
"PostToolUse": [
{
"matcher": "Edit|Write",
"hooks": [
{
"type": "command",
"command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/markdown_formatter.py"
}
]
}
]
}
}
`

使用以下内容创建 `.claude/hooks/markdown_formatter.py`：

报告错误代码

复制

询问AI

`#!/usr/bin/env python3
"""
Markdown formatter for Claude Code output.
Fixes missing language tags and spacing issues while preserving code content.
"""
import json
import sys
import re
import os

def detect_language(code):
"""Best-effort language detection from code content."""
s = code.strip()

# JSON detection
if re.search(r'^\s*[{\[]', s):
try:
json.loads(s)
return 'json'
except:
pass

# Python detection
if re.search(r'^\s*def\s+\w+\s*\(', s, re.M) or \
re.search(r'^\s*(import|from)\s+\w+', s, re.M):
return 'python'

# JavaScript detection
if re.search(r'\b(function\s+\w+\s*\(|const\s+\w+\s*=)', s) or \
re.search(r'=>|console\.(log|error)', s):
return 'javascript'

# Bash detection
if re.search(r'^#!.*\b(bash|sh)\b', s, re.M) or \
re.search(r'\b(if|then|fi|for|in|do|done)\b', s):
return 'bash'

# SQL detection
if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE|CREATE)\s+', s, re.I):
return 'sql'

return 'text'

def format_markdown(content):
"""Format markdown content with language detection."""
# Fix unlabeled code fences
def add_lang_to_fence(match):
indent, info, body, closing = match.groups()
if not info.strip():
lang = detect_language(body)
return f"{indent}```{lang}\n{body}{closing}\n"
return match.group(0)

fence_pattern = r'(?ms)^([ \t]{0,3})```([^\n]*)\n(.*?)(\n\1```)\s*$'
content = re.sub(fence_pattern, add_lang_to_fence, content)

# Fix excessive blank lines (only outside code fences)
content = re.sub(r'\n{3,}', '\n\n', content)

return content.rstrip() + '\n'

# Main execution
try:
input_data = json.load(sys.stdin)
file_path = input_data.get('tool_input', {}).get('file_path', '')

if not file_path.endswith(('.md', '.mdx')):
sys.exit(0)  # Not a markdown file

if os.path.exists(file_path):
with open(file_path, 'r', encoding='utf-8') as f:
content = f.read()

formatted = format_markdown(content)

if formatted != content:
with open(file_path, 'w', encoding='utf-8') as f:
f.write(formatted)
print(f"✓ Fixed markdown formatting in {file_path}")

except Exception as e:
print(f"Error formatting markdown: {e}", file=sys.stderr)
sys.exit(1)
`

使脚本可执行：

报告错误代码

复制

询问AI

`chmod +x .claude/hooks/markdown_formatter.py
`

此钩子自动：

- 检测未标记代码块中的编程语言

- 为语法突出显示添加适当的语言标签

- 修复过多的空行，同时保留代码内容

- 仅处理 markdown 文件（`.md`、`.mdx`）

###
[​

](#自定义通知钩子)
自定义通知钩子

当 Claude 需要输入时获得桌面通知：

报告错误代码

复制

询问AI

`{
"hooks": {
"Notification": [
{
"matcher": "",
"hooks": [
{
"type": "command",
"command": "notify-send 'Claude Code' 'Awaiting your input'"
}
]
}
]
}
}
`

###
[​

](#文件保护钩子)
文件保护钩子

阻止对敏感文件的编辑：

报告错误代码

复制

询问AI

`{
"hooks": {
"PreToolUse": [
{
"matcher": "Edit|Write",
"hooks": [
{
"type": "command",
"command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2 if any(p in path for p in ['.env', 'package-lock.json', '.git/']) else 0)\""
}
]
}
]
}
}
`

##
[​

](#了解更多)
了解更多

- 有关钩子的参考文档，请参阅 [钩子参考](/docs/zh-CN/hooks)。

- 有关全面的安全最佳实践和安全指南，请参阅钩子参考文档中的 [安全考虑](/docs/zh-CN/hooks#security-considerations)。

- 有关故障排除步骤和调试技术，请参阅钩子参考文档中的 [调试](/docs/zh-CN/hooks#debugging)。

此页面对您有帮助吗？

是否

[输出样式](/docs/zh-CN/output-styles)[编程使用](/docs/zh-CN/headless)

⌘I

助手

AI生成的回答可能包含错误。
