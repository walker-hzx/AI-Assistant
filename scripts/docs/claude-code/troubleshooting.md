# Troubleshooting 官方文档

> 来源: https://code.claude.com/docs/zh-CN/troubleshooting

> 爬取时间: 自动生成

---

- 故障排除 - Claude Code Docs

[跳转到主要内容](#content-area)

[Claude Code Docs home page](/docs)

简体中文

搜索...

⌘K询问AI

搜索...

Navigation

使用 Claude Code 构建

故障排除

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

- [常见安装问题](#%E5%B8%B8%E8%A7%81%E5%AE%89%E8%A3%85%E9%97%AE%E9%A2%98)
- [Windows 安装问题：WSL 中的错误](#windows-%E5%AE%89%E8%A3%85%E9%97%AE%E9%A2%98%EF%BC%9Awsl-%E4%B8%AD%E7%9A%84%E9%94%99%E8%AF%AF)
- [WSL2 sandbox 设置](#wsl2-sandbox-%E8%AE%BE%E7%BD%AE)
- [Linux 和 Mac 安装问题：权限或找不到命令错误](#linux-%E5%92%8C-mac-%E5%AE%89%E8%A3%85%E9%97%AE%E9%A2%98%EF%BC%9A%E6%9D%83%E9%99%90%E6%88%96%E6%89%BE%E4%B8%8D%E5%88%B0%E5%91%BD%E4%BB%A4%E9%94%99%E8%AF%AF)
- [推荐解决方案：原生 Claude Code 安装](#%E6%8E%A8%E8%8D%90%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%EF%BC%9A%E5%8E%9F%E7%94%9F-claude-code-%E5%AE%89%E8%A3%85)
- [Windows：“Claude Code on Windows requires git-bash”](#windows%EF%BC%9A%E2%80%9Cclaude-code-on-windows-requires-git-bash%E2%80%9D)
- [Windows：“installMethod is native, but claude command not found”](#windows%EF%BC%9A%E2%80%9Cinstallmethod-is-native-but-claude-command-not-found%E2%80%9D)
- [权限和身份验证](#%E6%9D%83%E9%99%90%E5%92%8C%E8%BA%AB%E4%BB%BD%E9%AA%8C%E8%AF%81)
- [重复的权限提示](#%E9%87%8D%E5%A4%8D%E7%9A%84%E6%9D%83%E9%99%90%E6%8F%90%E7%A4%BA)
- [身份验证问题](#%E8%BA%AB%E4%BB%BD%E9%AA%8C%E8%AF%81%E9%97%AE%E9%A2%98)
- [配置文件位置](#%E9%85%8D%E7%BD%AE%E6%96%87%E4%BB%B6%E4%BD%8D%E7%BD%AE)
- [重置配置](#%E9%87%8D%E7%BD%AE%E9%85%8D%E7%BD%AE)
- [性能和稳定性](#%E6%80%A7%E8%83%BD%E5%92%8C%E7%A8%B3%E5%AE%9A%E6%80%A7)
- [高 CPU 或内存使用率](#%E9%AB%98-cpu-%E6%88%96%E5%86%85%E5%AD%98%E4%BD%BF%E7%94%A8%E7%8E%87)
- [命令挂起或冻结](#%E5%91%BD%E4%BB%A4%E6%8C%82%E8%B5%B7%E6%88%96%E5%86%BB%E7%BB%93)
- [搜索和发现问题](#%E6%90%9C%E7%B4%A2%E5%92%8C%E5%8F%91%E7%8E%B0%E9%97%AE%E9%A2%98)
- [WSL 上的搜索结果缓慢或不完整](#wsl-%E4%B8%8A%E7%9A%84%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C%E7%BC%93%E6%85%A2%E6%88%96%E4%B8%8D%E5%AE%8C%E6%95%B4)
- [IDE 集成问题](#ide-%E9%9B%86%E6%88%90%E9%97%AE%E9%A2%98)
- [WSL2 上未检测到 JetBrains IDE](#wsl2-%E4%B8%8A%E6%9C%AA%E6%A3%80%E6%B5%8B%E5%88%B0-jetbrains-ide)
- [WSL2 网络模式](#wsl2-%E7%BD%91%E7%BB%9C%E6%A8%A1%E5%BC%8F)
- [报告 Windows IDE 集成问题（原生和 WSL）](#%E6%8A%A5%E5%91%8A-windows-ide-%E9%9B%86%E6%88%90%E9%97%AE%E9%A2%98%EF%BC%88%E5%8E%9F%E7%94%9F%E5%92%8C-wsl%EF%BC%89)
- [JetBrains（IntelliJ、PyCharm 等）终端中的 Escape 键不起作用](#jetbrains%EF%BC%88intellij%E3%80%81pycharm-%E7%AD%89%EF%BC%89%E7%BB%88%E7%AB%AF%E4%B8%AD%E7%9A%84-escape-%E9%94%AE%E4%B8%8D%E8%B5%B7%E4%BD%9C%E7%94%A8)
- [Markdown 格式问题](#markdown-%E6%A0%BC%E5%BC%8F%E9%97%AE%E9%A2%98)
- [代码块中缺少语言标签](#%E4%BB%A3%E7%A0%81%E5%9D%97%E4%B8%AD%E7%BC%BA%E5%B0%91%E8%AF%AD%E8%A8%80%E6%A0%87%E7%AD%BE)
- [不一致的间距和格式](#%E4%B8%8D%E4%B8%80%E8%87%B4%E7%9A%84%E9%97%B4%E8%B7%9D%E5%92%8C%E6%A0%BC%E5%BC%8F)
- [Markdown 生成的最佳实践](#markdown-%E7%94%9F%E6%88%90%E7%9A%84%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5)
- [获取更多帮助](#%E8%8E%B7%E5%8F%96%E6%9B%B4%E5%A4%9A%E5%B8%AE%E5%8A%A9)

##
[​

](#常见安装问题)
常见安装问题

###
[​

](#windows-安装问题：wsl-中的错误)
Windows 安装问题：WSL 中的错误

您可能会在 WSL 中遇到以下问题：
**操作系统/平台检测问题**：如果您在安装期间收到错误，WSL 可能正在使用 Windows `npm`。请尝试：

- 在安装前运行 `npm config set os linux`

- 使用 `npm install -g @anthropic-ai/claude-code --force --no-os-check` 进行安装（不要使用 `sudo`）

**找不到 Node 错误**：如果在运行 `claude` 时看到 `exec: node: not found`，您的 WSL 环境可能正在使用 Windows 安装的 Node.js。您可以使用 `which npm` 和 `which node` 来确认，它们应该指向以 `/usr/` 开头的 Linux 路径，而不是 `/mnt/c/`。要解决此问题，请尝试通过您的 Linux 发行版的包管理器或通过 [`nvm`](https://github.com/nvm-sh/nvm) 安装 Node。
**nvm 版本冲突**：如果您在 WSL 和 Windows 中都安装了 nvm，在 WSL 中切换 Node 版本时可能会遇到版本冲突。这是因为 WSL 默认导入 Windows PATH，导致 Windows nvm/npm 优先于 WSL 安装。
您可以通过以下方式识别此问题：

- 运行 `which npm` 和 `which node` - 如果它们指向 Windows 路径（以 `/mnt/c/` 开头），则正在使用 Windows 版本

- 在 WSL 中使用 nvm 切换 Node 版本后功能损坏

要解决此问题，请修复您的 Linux PATH 以确保 Linux node/npm 版本优先：
**主要解决方案：确保 nvm 在您的 shell 中正确加载**
最常见的原因是 nvm 未在非交互式 shell 中加载。将以下内容添加到您的 shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）：

报告错误代码

复制

询问AI

`# Load nvm if it exists
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
`

或在您的当前会话中直接运行：

报告错误代码

复制

询问AI

`source ~/.nvm/nvm.sh
`

**替代方案：调整 PATH 顺序**
如果 nvm 已正确加载但 Windows 路径仍然优先，您可以在 shell 配置中显式地将 Linux 路径添加到 PATH 的前面：

报告错误代码

复制

询问AI

`export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
`

避免禁用 Windows PATH 导入（`appendWindowsPath = false`），因为这会破坏从 WSL 调用 Windows 可执行文件的能力。同样，如果您在 Windows 开发中使用 Node.js，请避免从 Windows 卸载它。

###
[​

](#wsl2-sandbox-设置)
WSL2 sandbox 设置

[Sandboxing](/docs/zh-CN/sandboxing) 在 WSL2 上受支持，但需要安装额外的包。如果您在运行 `/sandbox` 时看到类似”Sandbox requires socat and bubblewrap”的错误，请安装依赖项：

-
Ubuntu/Debian

-
Fedora

报告错误代码

复制

询问AI

`sudo apt-get install bubblewrap socat
`

报告错误代码

复制

询问AI

`sudo dnf install bubblewrap socat
`

WSL1 不支持 sandboxing。如果您看到”Sandboxing requires WSL2”，您需要升级到 WSL2 或在没有 sandboxing 的情况下运行 Claude Code。
###
[​

](#linux-和-mac-安装问题：权限或找不到命令错误)
Linux 和 Mac 安装问题：权限或找不到命令错误

使用 npm 安装 Claude Code 时，`PATH` 问题可能会阻止访问 `claude`。
如果您的 npm 全局前缀不可由用户写入（例如 `/usr` 或 `/usr/local`），您也可能遇到权限错误。
####
[​

](#推荐解决方案：原生-claude-code-安装)
推荐解决方案：原生 Claude Code 安装

Claude Code 有一个不依赖于 npm 或 Node.js 的原生安装。
使用以下命令运行原生安装程序。
**macOS、Linux、WSL：**

报告错误代码

复制

询问AI

`# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
`

**Windows PowerShell：**

报告错误代码

复制

询问AI

`# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

`

此命令为您的操作系统和架构安装适当的 Claude Code 构建，并在 `~/.local/bin/claude`（或 Windows 上的 `%USERPROFILE%\.local\bin\claude.exe`）处添加安装的符号链接。

确保您的系统 PATH 中有安装目录。

###
[​

](#windows：“claude-code-on-windows-requires-git-bash”)
Windows：“Claude Code on Windows requires git-bash”

Windows 上的原生 Claude Code 需要 [Git for Windows](https://git-scm.com/downloads/win)，其中包括 Git Bash。如果已安装 Git 但未被检测到：

-
在运行 Claude 之前在 PowerShell 中显式设置路径：

报告错误代码

复制

询问AI

`$env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
`

-
或通过系统属性 → 环境变量将其永久添加到您的系统环境变量中。

如果 Git 安装在非标准位置，请相应地调整路径。
###
[​

](#windows：“installmethod-is-native-but-claude-command-not-found”)
Windows：“installMethod is native, but claude command not found”

如果您在安装后看到此错误，`claude` 命令不在您的 PATH 中。手动添加它：

1

[

](#)

打开环境变量

按 `Win + R`，输入 `sysdm.cpl`，然后按 Enter。单击**高级** → **环境变量**。

2

[

](#)

编辑用户 PATH

在”用户变量”下，选择**路径**并单击**编辑**。单击**新建**并添加：

报告错误代码

复制

询问AI

`%USERPROFILE%\.local\bin
`

3

[

](#)

重启您的终端

关闭并重新打开 PowerShell 或 CMD 以使更改生效。

验证安装：

报告错误代码

复制

询问AI

`claude doctor # Check installation health
`

##
[​

](#权限和身份验证)
权限和身份验证

###
[​

](#重复的权限提示)
重复的权限提示

如果您发现自己反复批准相同的命令，您可以使用 `/permissions` 命令允许特定工具在没有批准的情况下运行。请参阅[权限文档](/docs/zh-CN/permissions#manage-permissions)。
###
[​

](#身份验证问题)
身份验证问题

如果您遇到身份验证问题：

- 运行 `/logout` 完全注销

- 关闭 Claude Code

- 使用 `claude` 重新启动并再次完成身份验证过程

如果浏览器在登录期间不会自动打开，请按 `c` 将 OAuth URL 复制到您的剪贴板，然后手动将其粘贴到您的浏览器中。
如果问题仍然存在，请尝试：

报告错误代码

复制

询问AI

`rm -rf ~/.config/claude-code/auth.json
claude
`

这会删除您存储的身份验证信息并强制进行干净登录。
##
[​

](#配置文件位置)
配置文件位置

Claude Code 在多个位置存储配置：

| | 文件 | 目的 |
| `~/.claude/settings.json` | 用户设置（权限、hooks、模型覆盖） |
| `.claude/settings.json` | 项目设置（检入源代码控制） |
| `.claude/settings.local.json` | 本地项目设置（未提交） |
| `~/.claude.json` | 全局状态（主题、OAuth、MCP servers） |
| `.mcp.json` | 项目 MCP servers（检入源代码控制） |
| `managed-mcp.json` | [Managed MCP servers](/docs/zh-CN/mcp#managed-mcp-configuration) |
| Managed settings | [Managed settings](/docs/zh-CN/settings#settings-files)（服务器管理、MDM/OS 级别策略或基于文件） |

在 Windows 上，`~` 指的是您的用户主目录，例如 `C:\Users\YourName`。
有关配置这些文件的详细信息，请参阅[设置](/docs/zh-CN/settings)和 [MCP](/docs/zh-CN/mcp)。
###
[​

](#重置配置)
重置配置

要将 Claude Code 重置为默认设置，您可以删除配置文件：

报告错误代码

复制

询问AI

`# Reset all user settings and state
rm ~/.claude.json
rm -rf ~/.claude/

# Reset project-specific settings
rm -rf .claude/
rm .mcp.json
`

这将删除您的所有设置、MCP 服务器配置和会话历史记录。

##
[​

](#性能和稳定性)
性能和稳定性

###
[​

](#高-cpu-或内存使用率)
高 CPU 或内存使用率

Claude Code 设计用于与大多数开发环境配合使用，但在处理大型代码库时可能会消耗大量资源。如果您遇到性能问题：

- 定期使用 `/compact` 来减少上下文大小

- 在主要任务之间关闭并重新启动 Claude Code

- 考虑将大型构建目录添加到您的 `.gitignore` 文件中

###
[​

](#命令挂起或冻结)
命令挂起或冻结

如果 Claude Code 似乎无响应：

- 按 Ctrl+C 尝试取消当前操作

- 如果无响应，您可能需要关闭终端并重新启动

###
[​

](#搜索和发现问题)
搜索和发现问题

如果搜索工具、`@file` 提及、自定义代理和自定义技能不起作用，请安装系统 `ripgrep`：

报告错误代码

复制

询问AI

`# macOS (Homebrew)
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
`

然后在您的[环境](/docs/zh-CN/settings#environment-variables)中设置 `USE_BUILTIN_RIPGREP=0`。
###
[​

](#wsl-上的搜索结果缓慢或不完整)
WSL 上的搜索结果缓慢或不完整

在 WSL 上[跨文件系统工作](https://learn.microsoft.com/en-us/windows/wsl/filesystems)时的磁盘读取性能损失可能导致在 WSL 上使用 Claude Code 时匹配数少于预期（但不是完全缺乏搜索功能）。

在这种情况下，`/doctor` 会将搜索显示为正常。

**解决方案：**

-
**提交更具体的搜索**：通过指定目录或文件类型来减少搜索的文件数量：“Search for JWT validation logic in the auth-service package”或”Find use of md5 hash in JS files”。

-
**将项目移到 Linux 文件系统**：如果可能，确保您的项目位于 Linux 文件系统（`/home/`）而不是 Windows 文件系统（`/mnt/c/`）。

-
**改用原生 Windows**：考虑在 Windows 上原生运行 Claude Code 而不是通过 WSL，以获得更好的文件系统性能。

##
[​

](#ide-集成问题)
IDE 集成问题

###
[​

](#wsl2-上未检测到-jetbrains-ide)
WSL2 上未检测到 JetBrains IDE

如果您在 WSL2 上使用 Claude Code 和 JetBrains IDE，并收到”No available IDEs detected”错误，这可能是由于 WSL2 的网络配置或 Windows 防火墙阻止连接。
####
[​

](#wsl2-网络模式)
WSL2 网络模式

WSL2 默认使用 NAT 网络，这可能会阻止 IDE 检测。您有两个选项：
**选项 1：配置 Windows 防火墙**（推荐）

-
找到您的 WSL2 IP 地址：

报告错误代码

复制

询问AI

`wsl hostname -I
# Example output: 172.21.123.456
`

-
以管理员身份打开 PowerShell 并创建防火墙规则：

报告错误代码

复制

询问AI

`New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
`

（根据步骤 1 中的 WSL2 子网调整 IP 范围）

-
重新启动您的 IDE 和 Claude Code

**选项 2：切换到镜像网络**
添加到您的 Windows 用户目录中的 `.wslconfig`：

报告错误代码

复制

询问AI

`[wsl2]
networkingMode=mirrored
`

然后从 PowerShell 使用 `wsl --shutdown` 重新启动 WSL。

这些网络问题仅影响 WSL2。WSL1 直接使用主机的网络，不需要这些配置。

有关其他 JetBrains 配置提示，请参阅我们的 [JetBrains IDE 指南](/docs/zh-CN/jetbrains#plugin-settings)。
###
[​

](#报告-windows-ide-集成问题（原生和-wsl）)
报告 Windows IDE 集成问题（原生和 WSL）

如果您在 Windows 上遇到 IDE 集成问题，请[创建一个问题](https://github.com/anthropics/claude-code/issues)并提供以下信息：

- 环境类型：原生 Windows（Git Bash）或 WSL1/WSL2

- WSL 网络模式（如果适用）：NAT 或镜像

- IDE 名称和版本

- Claude Code 扩展/插件版本

- Shell 类型：Bash、Zsh、PowerShell 等

###
[​

](#jetbrains（intellij、pycharm-等）终端中的-escape-键不起作用)
JetBrains（IntelliJ、PyCharm 等）终端中的 Escape 键不起作用

如果您在 JetBrains 终端中使用 Claude Code，而 `Esc` 键不能按预期中断代理，这可能是由于与 JetBrains 默认快捷键的快捷键冲突。
要解决此问题：

- 转到设置 → 工具 → 终端

- 要么：

取消选中”Move focus to the editor with Escape”，或

- 单击”Configure terminal keybindings”并删除”Switch focus to Editor”快捷键

- 应用更改

这允许 `Esc` 键正确中断 Claude Code 操作。
##
[​

](#markdown-格式问题)
Markdown 格式问题

Claude Code 有时会生成 markdown 文件，代码围栏上缺少语言标签，这可能会影响 GitHub、编辑器和文档工具中的语法突出显示和可读性。
###
[​

](#代码块中缺少语言标签)
代码块中缺少语言标签

如果您在生成的 markdown 中注意到这样的代码块：

报告错误代码

复制

询问AI

````
function example() {
return "hello";
}
```
`

而不是正确标记的块，如：

报告错误代码

复制

询问AI

````javascript
function example() {
return "hello";
}
```
`

**解决方案：**

-
**要求 Claude 添加语言标签**：请求”Add appropriate language tags to all code blocks in this markdown file.”

-
**使用后处理 hooks**：设置自动格式化 hooks 来检测和添加缺失的语言标签。有关 PostToolUse 格式化 hook 的示例，请参阅[编辑后自动格式化代码](/docs/zh-CN/hooks-guide#auto-format-code-after-edits)。

-
**手动验证**：生成 markdown 文件后，查看它们以确保正确的代码块格式，如果需要，请求更正。

###
[​

](#不一致的间距和格式)
不一致的间距和格式

如果生成的 markdown 有过多的空行或不一致的间距：
**解决方案：**

-
**请求格式更正**：要求 Claude”Fix spacing and formatting issues in this markdown file.”

-
**使用格式化工具**：设置 hooks 以在生成的 markdown 文件上运行 markdown 格式化程序（如 `prettier`）或自定义格式化脚本。

-
**指定格式化首选项**：在您的提示或项目[内存](/docs/zh-CN/memory)文件中包含格式化要求。

###
[​

](#markdown-生成的最佳实践)
Markdown 生成的最佳实践

要最小化格式问题：

- **在请求中明确**：要求”properly formatted markdown with language-tagged code blocks”

- **使用项目约定**：在 [`CLAUDE.md`](/docs/zh-CN/memory) 中记录您首选的 markdown 样式

- **设置验证 hooks**：使用后处理 hooks 自动验证和修复常见格式问题

##
[​

](#获取更多帮助)
获取更多帮助

如果您遇到此处未涵盖的问题：

- 在 Claude Code 中使用 `/bug` 命令直接向 Anthropic 报告问题

- 检查 [GitHub 存储库](https://github.com/anthropics/claude-code)以了解已知问题

- 运行 `/doctor` 来诊断问题。它检查：

安装类型、版本和搜索功能

- 自动更新状态和可用版本

- 无效的设置文件（格式错误的 JSON、不正确的类型）

- MCP 服务器配置错误

- 快捷键配置问题

- 上下文使用警告（大型 CLAUDE.md 文件、高 MCP 令牌使用、无法访问的权限规则）

- 插件和代理加载错误

- 直接向 Claude 询问其功能和特性 - Claude 内置了对其文档的访问权限

此页面对您有帮助吗？

是否

[Model Context Protocol (MCP)](/docs/zh-CN/mcp)

⌘I

助手

AI生成的回答可能包含错误。
