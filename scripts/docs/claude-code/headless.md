# Headless 官方文档

> 来源: https://code.claude.com/docs/zh-CN/headless

> 爬取时间: 自动生成

---

- 以编程方式运行 Claude Code - Claude Code Docs

[跳转到主要内容](#content-area)

[Claude Code Docs home page](/docs)

简体中文

搜索...

⌘K询问AI

搜索...

Navigation

使用 Claude Code 构建

以编程方式运行 Claude Code

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

- [基本用法](#%E5%9F%BA%E6%9C%AC%E7%94%A8%E6%B3%95)
- [示例](#%E7%A4%BA%E4%BE%8B)
- [获取结构化输出](#%E8%8E%B7%E5%8F%96%E7%BB%93%E6%9E%84%E5%8C%96%E8%BE%93%E5%87%BA)
- [流式传输响应](#%E6%B5%81%E5%BC%8F%E4%BC%A0%E8%BE%93%E5%93%8D%E5%BA%94)
- [自动批准工具](#%E8%87%AA%E5%8A%A8%E6%89%B9%E5%87%86%E5%B7%A5%E5%85%B7)
- [创建提交](#%E5%88%9B%E5%BB%BA%E6%8F%90%E4%BA%A4)
- [自定义系统提示](#%E8%87%AA%E5%AE%9A%E4%B9%89%E7%B3%BB%E7%BB%9F%E6%8F%90%E7%A4%BA)
- [继续对话](#%E7%BB%A7%E7%BB%AD%E5%AF%B9%E8%AF%9D)
- [后续步骤](#%E5%90%8E%E7%BB%AD%E6%AD%A5%E9%AA%A4)

[Agent SDK](https://platform.claude.com/docs/zh-CN/agent-sdk/overview) 为您提供了支持 Claude Code 的相同工具、agent 循环和上下文管理。它可作为 CLI 用于脚本和 CI/CD，或作为 [Python](https://platform.claude.com/docs/zh-CN/agent-sdk/python) 和 [TypeScript](https://platform.claude.com/docs/zh-CN/agent-sdk/typescript) 包用于完整的编程控制。

CLI 之前称为”headless mode”。`-p` 标志和所有 CLI 选项的工作方式相同。

要从 CLI 以编程方式运行 Claude Code，请使用 `-p` 传递您的提示和任何 [CLI 选项](/docs/zh-CN/cli-reference)：

报告错误代码

复制

询问AI

`claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
`

本页介绍通过 CLI (`claude -p`) 使用 Agent SDK。对于具有结构化输出、工具批准回调和本机消息对象的 Python 和 TypeScript SDK 包，请参阅 [完整 Agent SDK 文档](https://platform.claude.com/docs/zh-CN/agent-sdk/overview)。
##
[​

](#基本用法)
基本用法

将 `-p`（或 `--print`）标志添加到任何 `claude` 命令以非交互方式运行它。所有 [CLI 选项](/docs/zh-CN/cli-reference) 都适用于 `-p`，包括：

- `--continue` 用于 [继续对话](#continue-conversations)

- `--allowedTools` 用于 [自动批准工具](#auto-approve-tools)

- `--output-format` 用于 [结构化输出](#get-structured-output)

此示例询问 Claude 关于您的代码库的问题并打印响应：

报告错误代码

复制

询问AI

`claude -p "What does the auth module do?"
`

##
[​

](#示例)
示例

这些示例突出了常见的 CLI 模式。
###
[​

](#获取结构化输出)
获取结构化输出

使用 `--output-format` 控制响应的返回方式：

- `text`（默认）：纯文本输出

- `json`：包含结果、会话 ID 和元数据的结构化 JSON

- `stream-json`：用于实时流式传输的换行符分隔的 JSON

此示例以 JSON 格式返回项目摘要以及会话元数据，文本结果在 `result` 字段中：

报告错误代码

复制

询问AI

`claude -p "Summarize this project" --output-format json
`

要获得符合特定架构的输出，请使用 `--output-format json` 与 `--json-schema` 和 [JSON Schema](https://json-schema.org/) 定义。响应包括关于请求的元数据（会话 ID、使用情况等），结构化输出在 `structured_output` 字段中。
此示例从 auth.py 中提取函数名称并将其作为字符串数组返回：

报告错误代码

复制

询问AI

`claude -p "Extract the main function names from auth.py" \
--output-format json \
--json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
`

使用 [jq](https://jqlang.github.io/jq/) 之类的工具来解析响应并提取特定字段：

报告错误代码

复制

询问AI

`# Extract the text result
claude -p "Summarize this project" --output-format json | jq -r '.result'

# Extract structured output
claude -p "Extract function names from auth.py" \
--output-format json \
--json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
| jq '.structured_output'
`

###
[​

](#流式传输响应)
流式传输响应

使用 `--output-format stream-json` 与 `--verbose` 和 `--include-partial-messages` 在生成令牌时接收它们。每一行都是代表一个事件的 JSON 对象：

报告错误代码

复制

询问AI

`claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
`

以下示例使用 [jq](https://jqlang.github.io/jq/) 过滤文本增量并仅显示流式文本。`-r` 标志输出原始字符串（无引号），`-j` 不带换行符连接，以便令牌连续流式传输：

报告错误代码

复制

询问AI

`claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
`

有关具有回调和消息对象的编程流式传输，请参阅 Agent SDK 文档中的 [实时流式传输响应](https://platform.claude.com/docs/zh-CN/agent-sdk/streaming-output)。
###
[​

](#自动批准工具)
自动批准工具

使用 `--allowedTools` 让 Claude 使用某些工具而无需提示。此示例运行测试套件并修复失败，允许 Claude 执行 Bash 命令和读取/编辑文件而无需请求权限：

报告错误代码

复制

询问AI

`claude -p "Run the test suite and fix any failures" \
--allowedTools "Bash,Read,Edit"
`

###
[​

](#创建提交)
创建提交

此示例审查暂存的更改并创建具有适当消息的提交：

报告错误代码

复制

询问AI

`claude -p "Look at my staged changes and create an appropriate commit" \
--allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
`

`--allowedTools` 标志使用 [权限规则语法](/docs/zh-CN/settings#permission-rule-syntax)。尾部的 ` *` 启用前缀匹配，因此 `Bash(git diff *)` 允许任何以 `git diff` 开头的命令。空格在 `*` 之前很重要：没有它，`Bash(git diff*)` 也会匹配 `git diff-index`。

用户调用的 [skills](/docs/zh-CN/skills) 如 `/commit` 和 [内置命令](/docs/zh-CN/interactive-mode#built-in-commands) 仅在交互模式中可用。在 `-p` 模式中，改为描述您想要完成的任务。

###
[​

](#自定义系统提示)
自定义系统提示

使用 `--append-system-prompt` 添加指令同时保持 Claude Code 的默认行为。此示例将 PR diff 传递给 Claude 并指示它审查安全漏洞：

报告错误代码

复制

询问AI

`gh pr diff "$1" | claude -p \
--append-system-prompt "You are a security engineer. Review for vulnerabilities." \
--output-format json
`

有关更多选项（包括 `--system-prompt` 以完全替换默认提示），请参阅 [系统提示标志](/docs/zh-CN/cli-reference#system-prompt-flags)。
###
[​

](#继续对话)
继续对话

使用 `--continue` 继续最近的对话，或使用 `--resume` 与会话 ID 继续特定对话。此示例运行审查，然后发送后续提示：

报告错误代码

复制

询问AI

`# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
`

如果您运行多个对话，请捕获会话 ID 以恢复特定对话：

报告错误代码

复制

询问AI

`session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
`

##
[​

](#后续步骤)
后续步骤

[

## Agent SDK 快速入门

使用 Python 或 TypeScript 构建您的第一个 agent

](https://platform.claude.com/docs/zh-CN/agent-sdk/quickstart)[

## CLI 参考

探索所有 CLI 标志和选项

](/docs/zh-CN/cli-reference)[

## GitHub Actions

在 GitHub 工作流中使用 Agent SDK

](/docs/zh-CN/github-actions)[

## GitLab CI/CD

在 GitLab 管道中使用 Agent SDK

](/docs/zh-CN/gitlab-ci-cd)

此页面对您有帮助吗？

是否

[Claude Code 钩子入门](/docs/zh-CN/hooks-guide)[Model Context Protocol (MCP)](/docs/zh-CN/mcp)

⌘I

助手

AI生成的回答可能包含错误。
