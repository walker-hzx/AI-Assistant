# Agent Teams 官方文档

> 来源: https://code.claude.com/docs/zh-CN/agent-teams

> 爬取时间: 自动生成

---

- 协调 Claude Code 会话团队 - Claude Code Docs

[跳转到主要内容](#content-area)

[Claude Code Docs home page](/docs)

简体中文

搜索...

⌘K询问AI

搜索...

Navigation

使用 Claude Code 构建

协调 Claude Code 会话团队

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

- [何时使用 agent teams](#%E4%BD%95%E6%97%B6%E4%BD%BF%E7%94%A8-agent-teams)
- [与 subagents 比较](#%E4%B8%8E-subagents-%E6%AF%94%E8%BE%83)
- [启用 agent teams](#%E5%90%AF%E7%94%A8-agent-teams)
- [启动你的第一个 agent team](#%E5%90%AF%E5%8A%A8%E4%BD%A0%E7%9A%84%E7%AC%AC%E4%B8%80%E4%B8%AA-agent-team)
- [控制你的 agent team](#%E6%8E%A7%E5%88%B6%E4%BD%A0%E7%9A%84-agent-team)
- [选择显示模式](#%E9%80%89%E6%8B%A9%E6%98%BE%E7%A4%BA%E6%A8%A1%E5%BC%8F)
- [指定队友和模型](#%E6%8C%87%E5%AE%9A%E9%98%9F%E5%8F%8B%E5%92%8C%E6%A8%A1%E5%9E%8B)
- [要求队友的计划批准](#%E8%A6%81%E6%B1%82%E9%98%9F%E5%8F%8B%E7%9A%84%E8%AE%A1%E5%88%92%E6%89%B9%E5%87%86)
- [直接与队友交谈](#%E7%9B%B4%E6%8E%A5%E4%B8%8E%E9%98%9F%E5%8F%8B%E4%BA%A4%E8%B0%88)
- [分配和认领任务](#%E5%88%86%E9%85%8D%E5%92%8C%E8%AE%A4%E9%A2%86%E4%BB%BB%E5%8A%A1)
- [关闭队友](#%E5%85%B3%E9%97%AD%E9%98%9F%E5%8F%8B)
- [清理团队](#%E6%B8%85%E7%90%86%E5%9B%A2%E9%98%9F)
- [使用 hooks 强制质量门](#%E4%BD%BF%E7%94%A8-hooks-%E5%BC%BA%E5%88%B6%E8%B4%A8%E9%87%8F%E9%97%A8)
- [Agent teams 如何工作](#agent-teams-%E5%A6%82%E4%BD%95%E5%B7%A5%E4%BD%9C)
- [Claude 如何启动 agent teams](#claude-%E5%A6%82%E4%BD%95%E5%90%AF%E5%8A%A8-agent-teams)
- [架构](#%E6%9E%B6%E6%9E%84)
- [权限](#%E6%9D%83%E9%99%90)
- [Context 和通信](#context-%E5%92%8C%E9%80%9A%E4%BF%A1)
- [令牌使用](#%E4%BB%A4%E7%89%8C%E4%BD%BF%E7%94%A8)
- [用例示例](#%E7%94%A8%E4%BE%8B%E7%A4%BA%E4%BE%8B)
- [运行并行代码审查](#%E8%BF%90%E8%A1%8C%E5%B9%B6%E8%A1%8C%E4%BB%A3%E7%A0%81%E5%AE%A1%E6%9F%A5)
- [使用竞争假设进行调查](#%E4%BD%BF%E7%94%A8%E7%AB%9E%E4%BA%89%E5%81%87%E8%AE%BE%E8%BF%9B%E8%A1%8C%E8%B0%83%E6%9F%A5)
- [最佳实践](#%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5)
- [给队友足够的 context](#%E7%BB%99%E9%98%9F%E5%8F%8B%E8%B6%B3%E5%A4%9F%E7%9A%84-context)
- [选择适当的团队规模](#%E9%80%89%E6%8B%A9%E9%80%82%E5%BD%93%E7%9A%84%E5%9B%A2%E9%98%9F%E8%A7%84%E6%A8%A1)
- [适当调整任务大小](#%E9%80%82%E5%BD%93%E8%B0%83%E6%95%B4%E4%BB%BB%E5%8A%A1%E5%A4%A7%E5%B0%8F)
- [等待队友完成](#%E7%AD%89%E5%BE%85%E9%98%9F%E5%8F%8B%E5%AE%8C%E6%88%90)
- [从研究和审查开始](#%E4%BB%8E%E7%A0%94%E7%A9%B6%E5%92%8C%E5%AE%A1%E6%9F%A5%E5%BC%80%E5%A7%8B)
- [避免文件冲突](#%E9%81%BF%E5%85%8D%E6%96%87%E4%BB%B6%E5%86%B2%E7%AA%81)
- [监控和指导](#%E7%9B%91%E6%8E%A7%E5%92%8C%E6%8C%87%E5%AF%BC)
- [故障排除](#%E6%95%85%E9%9A%9C%E6%8E%92%E9%99%A4)
- [队友未出现](#%E9%98%9F%E5%8F%8B%E6%9C%AA%E5%87%BA%E7%8E%B0)
- [太多权限提示](#%E5%A4%AA%E5%A4%9A%E6%9D%83%E9%99%90%E6%8F%90%E7%A4%BA)
- [队友在错误时停止](#%E9%98%9F%E5%8F%8B%E5%9C%A8%E9%94%99%E8%AF%AF%E6%97%B6%E5%81%9C%E6%AD%A2)
- [负责人在工作完成前关闭](#%E8%B4%9F%E8%B4%A3%E4%BA%BA%E5%9C%A8%E5%B7%A5%E4%BD%9C%E5%AE%8C%E6%88%90%E5%89%8D%E5%85%B3%E9%97%AD)
- [孤立的 tmux 会话](#%E5%AD%A4%E7%AB%8B%E7%9A%84-tmux-%E4%BC%9A%E8%AF%9D)
- [限制](#%E9%99%90%E5%88%B6)
- [后续步骤](#%E5%90%8E%E7%BB%AD%E6%AD%A5%E9%AA%A4)

Agent teams 是实验性功能，默认禁用。通过将 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 添加到你的 [settings.json](/docs/zh-CN/settings) 或环境变量来启用它们。Agent teams 在 [已知限制](#limitations) 中存在关于会话恢复、任务协调和关闭行为的问题。

Agent teams 让你协调多个 Claude Code 实例一起工作。一个会话充当团队负责人，协调工作、分配任务和综合结果。队友独立工作，每个都在自己的 context window 中，并直接相互通信。
与 [subagents](/docs/zh-CN/sub-agents) 不同，subagents 在单个会话中运行，只能向主代理报告，你也可以直接与个别队友互动，无需通过负责人。
本页涵盖：

- [何时使用 agent teams](#when-to-use-agent-teams)，包括最佳用例以及它们与 subagents 的比较

- [启动团队](#start-your-first-agent-team)

- [控制队友](#control-your-agent-team)，包括显示模式、任务分配和委派

- [并行工作的最佳实践](#best-practices)

##
[​

](#何时使用-agent-teams)
何时使用 agent teams

Agent teams 最适合用于并行探索能增加真实价值的任务。查看 [用例示例](#use-case-examples) 了解完整场景。最强的用例是：

- **研究和审查**：多个队友可以同时调查问题的不同方面，然后分享和质疑彼此的发现

- **新模块或功能**：队友可以各自拥有一个独立的部分，不会相互干扰

- **使用竞争假设进行调试**：队友并行测试不同的理论，更快地收敛到答案

- **跨层协调**：跨越前端、后端和测试的更改，每个由不同的队友负责

Agent teams 增加了协调开销，使用的令牌数量明显多于单个会话。当队友可以独立运作时，它们效果最好。对于顺序任务、同一文件编辑或有许多依赖关系的工作，单个会话或 [subagents](/docs/zh-CN/sub-agents) 更有效。
###
[​

](#与-subagents-比较)
与 subagents 比较

Agent teams 和 [subagents](/docs/zh-CN/sub-agents) 都让你并行化工作，但它们的运作方式不同。根据你的工作人员是否需要相互通信来选择：

Subagents 只向主代理报告结果，彼此不交谈。在 agent teams 中，队友共享任务列表、认领工作并直接相互通信。

| |  | Subagents | Agent teams |
| **Context** | 自己的 context window；结果返回给调用者 | 自己的 context window；完全独立 |
| **通信** | 仅向主代理报告结果 | 队友直接相互发送消息 |
| **协调** | 主代理管理所有工作 | 共享任务列表，自我协调 |
| **最适合** | 只有结果重要的专注任务 | 需要讨论和协作的复杂工作 |
| **令牌成本** | 较低：结果汇总回主 context | 较高：每个队友是一个独立的 Claude 实例 |

当你需要快速、专注的工作人员报告结果时，使用 subagents。当队友需要分享发现、相互质疑和自我协调时，使用 agent teams。
##
[​

](#启用-agent-teams)
启用 agent teams

Agent teams 默认禁用。通过将 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 环境变量设置为 `1` 来启用它们，可以在你的 shell 环境中或通过 [settings.json](/docs/zh-CN/settings) 进行设置：

settings.json

报告错误代码

复制

询问AI

`{
"env": {
"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
}
}
`

##
[​

](#启动你的第一个-agent-team)
启动你的第一个 agent team

启用 agent teams 后，告诉 Claude 创建一个 agent team，并用自然语言描述你想要的任务和团队结构。Claude 创建团队、生成队友并根据你的提示协调工作。
这个例子效果很好，因为三个角色是独立的，可以在不相互等待的情况下探索问题：

报告错误代码

复制

询问AI

`I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
`

从那里，Claude 创建一个具有 [共享任务列表](/docs/zh-CN/interactive-mode#task-list) 的团队，为每个角度生成队友，让他们探索问题，综合发现，并尝试在完成时 [清理团队](#clean-up-the-team)。
负责人的终端列出所有队友及其正在处理的工作。使用 Shift+Down 循环浏览队友并直接向他们发送消息。在最后一个队友之后，Shift+Down 会回到负责人。
如果你想让每个队友在自己的分割窗格中，请参阅 [选择显示模式](#choose-a-display-mode)。
##
[​

](#控制你的-agent-team)
控制你的 agent team

用自然语言告诉负责人你想要什么。它根据你的指示处理团队协调、任务分配和委派。
###
[​

](#选择显示模式)
选择显示模式

Agent teams 支持两种显示模式：

- **In-process**：所有队友在你的主终端内运行。使用 Shift+Down 循环浏览队友并输入直接向他们发送消息。在任何终端中工作，无需额外设置。

- **Split panes**：每个队友获得自己的窗格。你可以同时看到每个人的输出，并点击窗格直接交互。需要 tmux 或 iTerm2。

`tmux` 在某些操作系统上有已知限制，传统上在 macOS 上效果最好。在 iTerm2 中使用 `tmux -CC` 是进入 `tmux` 的建议入口点。

默认值是 `"auto"`，如果你已经在 tmux 会话中运行，则使用分割窗格，否则使用 in-process。`"tmux"` 设置启用分割窗格模式，并根据你的终端自动检测是使用 tmux 还是 iTerm2。要覆盖，在你的 [settings.json](/docs/zh-CN/settings) 中设置 `teammateMode`：

报告错误代码

复制

询问AI

`{
"teammateMode": "in-process"
}
`

要为单个会话强制 in-process 模式，将其作为标志传递：

报告错误代码

复制

询问AI

`claude --teammate-mode in-process
`

分割窗格模式需要 [tmux](https://github.com/tmux/tmux/wiki) 或 iTerm2 与 [`it2` CLI](https://github.com/mkusaka/it2)。手动安装：

- **tmux**：通过你的系统包管理器安装。查看 [tmux wiki](https://github.com/tmux/tmux/wiki/Installing) 了解特定于平台的说明。

- **iTerm2**：安装 [`it2` CLI](https://github.com/mkusaka/it2)，然后在 **iTerm2 → Settings → General → Magic → Enable Python API** 中启用 Python API。

###
[​

](#指定队友和模型)
指定队友和模型

Claude 根据你的任务决定要生成的队友数量，或者你可以指定你想要的确切内容：

报告错误代码

复制

询问AI

`Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
`

###
[​

](#要求队友的计划批准)
要求队友的计划批准

对于复杂或有风险的任务，你可以要求队友在实施前进行规划。队友在只读 Plan Mode 中工作，直到负责人批准他们的方法：

报告错误代码

复制

询问AI

`Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
`

当队友完成规划时，它向负责人发送计划批准请求。负责人审查计划并批准或拒绝并提供反馈。如果被拒绝，队友保持在 Plan Mode 中，根据反馈进行修订，并重新提交。一旦批准，队友退出 Plan Mode 并开始实施。
负责人自主做出批准决定。要影响负责人的判断，在你的提示中给出标准，例如”仅批准包含测试覆盖的计划”或”拒绝修改数据库架构的计划”。
###
[​

](#直接与队友交谈)
直接与队友交谈

每个队友都是一个完整的、独立的 Claude Code 会话。你可以直接向任何队友发送消息，以提供额外的指示、提出后续问题或改变他们的方法。

- **In-process 模式**：使用 Shift+Down 循环浏览队友，然后输入向他们发送消息。按 Enter 查看队友的会话，然后按 Escape 中断他们的当前轮次。按 Ctrl+T 切换任务列表。

- **Split-pane 模式**：点击队友的窗格直接与他们的会话交互。每个队友都有自己终端的完整视图。

###
[​

](#分配和认领任务)
分配和认领任务

共享任务列表协调整个团队的工作。负责人创建任务，队友完成它们。任务有三种状态：待处理、进行中和已完成。任务也可以依赖其他任务：具有未解决依赖关系的待处理任务在这些依赖关系完成之前无法被认领。
负责人可以显式分配任务，或队友可以自我认领：

- **负责人分配**：告诉负责人将哪个任务分配给哪个队友

- **自我认领**：完成任务后，队友自己选择下一个未分配、未阻止的任务

任务认领使用文件锁定来防止多个队友同时尝试认领同一任务时的竞态条件。
###
[​

](#关闭队友)
关闭队友

要优雅地结束队友的会话：

报告错误代码

复制

询问AI

`Ask the researcher teammate to shut down
`

负责人发送关闭请求。队友可以批准，优雅地退出，或拒绝并提供解释。
###
[​

](#清理团队)
清理团队

完成后，要求负责人清理：

报告错误代码

复制

询问AI

`Clean up the team
`

这会删除共享的团队资源。当负责人运行清理时，它会检查活跃的队友，如果有任何仍在运行，则失败，所以先关闭他们。

始终使用负责人进行清理。队友不应该运行清理，因为他们的团队 context 可能无法正确解析，可能会使资源处于不一致的状态。

###
[​

](#使用-hooks-强制质量门)
使用 hooks 强制质量门

使用 [hooks](/docs/zh-CN/hooks) 在队友完成工作或任务完成时强制执行规则：

- [`TeammateIdle`](/docs/zh-CN/hooks#teammateidle)：当队友即将空闲时运行。以代码 2 退出以发送反馈并保持队友工作。

- [`TaskCompleted`](/docs/zh-CN/hooks#taskcompleted)：当任务被标记为完成时运行。以代码 2 退出以防止完成并发送反馈。

##
[​

](#agent-teams-如何工作)
Agent teams 如何工作

本部分涵盖 agent teams 背后的架构和机制。如果你想开始使用它们，请参阅上面的 [控制你的 agent team](#control-your-agent-team)。
###
[​

](#claude-如何启动-agent-teams)
Claude 如何启动 agent teams

Agent teams 有两种启动方式：

- **你请求一个团队**：给 Claude 一个受益于并行工作的任务，并明确要求一个 agent team。Claude 根据你的指示创建一个。

- **Claude 提议一个团队**：如果 Claude 确定你的任务将受益于并行工作，它可能会建议创建一个团队。你在它继续之前确认。

在这两种情况下，你都保持控制。Claude 不会在没有你的批准的情况下创建团队。
###
[​

](#架构)
架构

Agent team 由以下部分组成：

| | 组件 | 角色 |
| **Team lead** | 创建团队、生成队友并协调工作的主 Claude Code 会话 |
| **Teammates** | 各自处理分配任务的独立 Claude Code 实例 |
| **Task list** | 队友认领和完成的共享工作项列表 |
| **Mailbox** | 代理之间通信的消息系统 |

查看 [选择显示模式](#choose-a-display-mode) 了解显示配置选项。队友消息自动到达负责人。
系统自动管理任务依赖关系。当队友完成其他任务依赖的任务时，被阻止的任务会自动解除阻止。
团队和任务存储在本地：

- **Team config**：`~/.claude/teams/{team-name}/config.json`

- **Task list**：`~/.claude/tasks/{team-name}/`

团队配置包含一个 `members` 数组，其中包含每个队友的名称、代理 ID 和代理类型。队友可以读取此文件以发现其他团队成员。
###
[​

](#权限)
权限

队友从负责人的权限设置开始。如果负责人使用 `--dangerously-skip-permissions` 运行，所有队友也会这样做。生成后，你可以更改个别队友的模式，但在生成时无法设置每个队友的模式。
###
[​

](#context-和通信)
Context 和通信

每个队友都有自己的 context window。生成时，队友加载与常规会话相同的项目 context：CLAUDE.md、MCP servers 和 skills。它还从负责人接收生成提示。负责人的对话历史不会继续。
**队友如何共享信息：**

- **自动消息传递**：当队友发送消息时，它们会自动传递给收件人。负责人不需要轮询更新。

- **空闲通知**：当队友完成并停止时，他们会自动通知负责人。

- **共享任务列表**：所有代理都可以看到任务状态并认领可用工作。

**队友消息传递：**

- **message**：向一个特定的队友发送消息

- **broadcast**：同时发送给所有队友。谨慎使用，因为成本随团队规模而增加。

###
[​

](#令牌使用)
令牌使用

Agent teams 使用的令牌数量明显多于单个会话。每个队友都有自己的 context window，令牌使用量随活跃队友的数量而增加。对于研究、审查和新功能工作，额外的令牌通常是值得的。对于日常任务，单个会话更具成本效益。查看 [agent team 令牌成本](/docs/zh-CN/costs#agent-team-token-costs) 了解使用指导。
##
[​

](#用例示例)
用例示例

这些示例展示了 agent teams 如何处理并行探索增加价值的任务。
###
[​

](#运行并行代码审查)
运行并行代码审查

单个审查者往往一次只关注一种类型的问题。将审查标准分解为独立的领域意味着安全性、性能和测试覆盖都同时获得彻底的关注。提示为每个队友分配一个不同的视角，以便他们不重叠：

报告错误代码

复制

询问AI

`Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
`

每个审查者从同一个 PR 工作，但应用不同的过滤器。负责人在他们完成后综合所有三个的发现。
###
[​

](#使用竞争假设进行调查)
使用竞争假设进行调查

当根本原因不清楚时，单个代理往往会找到一个看似合理的解释并停止寻找。提示通过让队友明确对抗来对抗这一点：每个队友的工作不仅是调查自己的理论，还要质疑其他队友的理论。

报告错误代码

复制

询问AI

`Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
`

辩论结构是这里的关键机制。顺序调查受到锚定的影响：一旦探索了一个理论，后续调查就会偏向于它。
有多个独立的调查者积极尝试相互反驳，存活下来的理论更有可能是实际的根本原因。
##
[​

](#最佳实践)
最佳实践

###
[​

](#给队友足够的-context)
给队友足够的 context

队友自动加载项目 context，包括 CLAUDE.md、MCP servers 和 skills，但他们不继承负责人的对话历史。查看 [Context 和通信](#context-and-communication) 了解详情。在生成提示中包含特定于任务的详情：

报告错误代码

复制

询问AI

`Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
`

###
[​

](#选择适当的团队规模)
选择适当的团队规模

队友数量没有硬限制，但实际约束适用：

- **令牌成本线性增加**：每个队友都有自己的 context window 并独立消耗令牌。查看 [agent team 令牌成本](/docs/zh-CN/costs#agent-team-token-costs) 了解详情。

- **协调开销增加**：更多队友意味着更多通信、任务协调和潜在冲突

- **收益递减**：超过一定点，额外的队友不会按比例加快工作

对于大多数工作流，从 3-5 个队友开始。这平衡了并行工作与可管理的协调。本指南中的示例使用 3-5 个队友，因为该范围在不同任务类型中效果很好。
每个队友有 5-6 个 [tasks](/docs/zh-CN/agent-teams#architecture) 可以保持每个人的生产力，而不会过度的上下文切换。如果你有 15 个独立任务，3 个队友是一个很好的起点。
仅当工作真正受益于队友同时工作时才扩展。三个专注的队友通常胜过五个分散的队友。
###
[​

](#适当调整任务大小)
适当调整任务大小

- **太小**：协调开销超过收益

- **太大**：队友工作太长时间而不进行检查，增加浪费努力的风险

- **恰到好处**：自包含的单位，产生清晰的可交付成果，例如函数、测试文件或审查

负责人将工作分解为任务并自动分配给队友。如果它没有创建足够的任务，要求它将工作分成更小的部分。每个队友有 5-6 个任务可以保持每个人的生产力，并让负责人在有人卡住时重新分配工作。

###
[​

](#等待队友完成)
等待队友完成

有时负责人开始自己实施任务，而不是等待队友。如果你注意到这一点：

报告错误代码

复制

询问AI

`Wait for your teammates to complete their tasks before proceeding
`

###
[​

](#从研究和审查开始)
从研究和审查开始

如果你是 agent teams 的新手，从具有明确边界且不需要编写代码的任务开始：审查 PR、研究库或调查错误。这些任务展示了并行探索的价值，而不会带来并行实施所带来的协调挑战。
###
[​

](#避免文件冲突)
避免文件冲突

两个队友编辑同一文件会导致覆盖。分解工作，使每个队友拥有不同的文件集。
###
[​

](#监控和指导)
监控和指导

检查队友的进度，重定向不起作用的方法，并在发现时综合发现。让团队无人值守运行太长时间会增加浪费努力的风险。
##
[​

](#故障排除)
故障排除

###
[​

](#队友未出现)
队友未出现

如果在你要求 Claude 创建团队后队友没有出现：

- 在 in-process 模式中，队友可能已经在运行但不可见。按 Shift+Down 循环浏览活跃的队友。

- 检查你给 Claude 的任务是否足够复杂以保证一个团队。Claude 根据任务决定是否生成队友。

- 如果你明确要求分割窗格，确保 tmux 已安装并在你的 PATH 中可用：

报告错误代码

复制

询问AI

`which tmux
`

- 对于 iTerm2，验证 `it2` CLI 已安装，并在 iTerm2 偏好设置中启用了 Python API。

###
[​

](#太多权限提示)
太多权限提示

队友权限请求冒泡到负责人，这可能会造成摩擦。在生成队友之前，在你的 [权限设置](/docs/zh-CN/permissions) 中预批准常见操作，以减少中断。
###
[​

](#队友在错误时停止)
队友在错误时停止

队友可能在遇到错误后停止，而不是恢复。在 in-process 模式中使用 Shift+Down 或在分割模式中点击窗格来检查他们的输出，然后：

- 直接给他们额外的指示

- 生成一个替代队友来继续工作

###
[​

](#负责人在工作完成前关闭)
负责人在工作完成前关闭

负责人可能会在所有任务实际完成之前决定团队已完成。如果发生这种情况，告诉它继续。你也可以告诉负责人在继续之前等待队友完成，如果它开始做工作而不是委派。
###
[​

](#孤立的-tmux-会话)
孤立的 tmux 会话

如果 tmux 会话在团队结束后仍然存在，它可能没有被完全清理。列出会话并杀死由团队创建的会话：

报告错误代码

复制

询问AI

`tmux ls
tmux kill-session -t <session-name>
`

##
[​

](#限制)
限制

Agent teams 是实验性的。需要注意的当前限制：

- **In-process 队友没有会话恢复**：`/resume` 和 `/rewind` 不会恢复 in-process 队友。恢复会话后，负责人可能会尝试向不再存在的队友发送消息。如果发生这种情况，告诉负责人生成新的队友。

- **任务状态可能滞后**：队友有时无法将任务标记为已完成，这会阻止依赖任务。如果任务似乎卡住，检查工作是否实际完成，并手动更新任务状态或告诉负责人推动队友。

- **关闭可能很慢**：队友在关闭前完成他们的当前请求或工具调用，这可能需要时间。

- **每个会话一个团队**：负责人一次只能管理一个团队。在启动新团队之前清理当前团队。

- **没有嵌套团队**：队友无法生成自己的团队或队友。只有负责人可以管理团队。

- **负责人是固定的**：创建团队的会话在其生命周期内是负责人。你无法将队友提升为负责人或转移领导权。

- **权限在生成时设置**：所有队友从负责人的权限模式开始。你可以在生成后更改个别队友的模式，但在生成时无法设置每个队友的模式。

- **分割窗格需要 tmux 或 iTerm2**：默认 in-process 模式在任何终端中工作。分割窗格模式在 VS Code 的集成终端、Windows Terminal 或 Ghostty 中不受支持。

**`CLAUDE.md` 正常工作**：队友从他们的工作目录读取 `CLAUDE.md` 文件。使用这个为所有队友提供项目特定的指导。

##
[​

](#后续步骤)
后续步骤

探索并行工作和委派的相关方法：

- **轻量级委派**：[subagents](/docs/zh-CN/sub-agents) 在你的会话中生成助手代理进行研究或验证，更适合不需要代理间协调的任务

- **手动并行会话**：[Git worktrees](/docs/zh-CN/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 让你自己运行多个 Claude Code 会话，无需自动化团队协调

- **比较方法**：查看 [subagent vs agent team](/docs/zh-CN/features-overview#compare-similar-features) 比较以获得并排分解

此页面对您有帮助吗？

是否

[创建自定义 subagents](/docs/zh-CN/sub-agents)[创建插件](/docs/zh-CN/plugins)

⌘I

助手

AI生成的回答可能包含错误。
