# 交互模式 - Claude Code

**来源**: https://code.claude.com/docs/zh-CN/interactive-mode

> Claude Code 交互模式参考，包括键盘快捷键、内置命令和交互功能。

---

## 目录

- [键盘快捷键](#键盘快捷键)
  - [常规控制](#常规控制)
  - [文本编辑](#文本编辑)
  - [主题和显示](#主题和显示)
  - [多行输入](#多行输入)
  - [快速命令](#快速命令)
- [内置命令](#内置命令)
- [Vim 编辑器模式](#vim-编辑器模式)
- [命令历史](#命令历史)
- [后台 bash 命令](#后台-bash-命令)
- [使用 ! 前缀的 Bash 模式](#使用--前缀的-bash-模式)
- [提示建议](#提示建议)
- [任务列表](#任务列表)
- [PR 审查状态](#pr-审查状态)

---

## 键盘快捷键

### macOS 配置

macOS 用户需要将 Option 配置为 Meta 才能使用某些快捷键：

- **iTerm2**: 设置 -> 配置文件 -> 键 -> 将左/右 Option 键设置为"Esc+"
- **Terminal.app**: 设置 -> 配置文件 -> 键盘 -> 勾选"使用 Option 作为 Meta 键"
- **VS Code**: 设置 -> 配置文件 -> 键 -> 将左/右 Option 键设置为"Esc+"

### 常规控制

| 快捷键 | 描述 | 上下文 |
|--------|------|--------|
| Ctrl+C | 取消当前输入或生成 | 标准中断 |
| Ctrl+F | 终止所有后台代理 | 后台代理控制 |
| Ctrl+D | 退出 Claude Code 会话 | EOF 信号 |
| Ctrl+G | 在默认文本编辑器中打开 | 编辑提示或响应 |
| Ctrl+L | 清除终端屏幕 | 保留对话历史 |
| Ctrl+O | 切换详细输出 | 显示详细工具使用 |
| Ctrl+R | 反向搜索命令历史 | 交互式搜索 |
| Ctrl+V | 从剪贴板粘贴图像 | 粘贴图像或路径 |
| Ctrl+B | 后台运行任务 | 后台 bash 命令 |
| Ctrl+T | 切换任务列表 | 显示/隐藏任务列表 |
| Left/Right arrows | 在对话框选项卡之间循环 | 权限对话框和菜单 |
| Up/Down arrows | 导航命令历史 | 回忆以前输入 |
| Esc + Esc | 回退或总结 | 恢复代码/对话 |
| Shift+Tab | 切换权限模式 | 自动接受/Plan/正常模式 |
| Option+P | 切换模型 | 切换 AI 模型 |
| Option+T | 切换扩展思考 | 启用/禁用扩展思考模式 |

### 文本编辑

| 快捷键 | 描述 | 上下文 |
|--------|------|--------|
| Ctrl+K | 删除到行尾 | 存储已删除的文本 |
| Ctrl+U | 删除整行 | 存储已删除的文本 |
| Ctrl+Y | 粘贴已删除的文本 | 粘贴 Ctrl+K/U 删除的 |
| Alt+Y | 循环粘贴历史 | 粘贴后循环浏览 |
| Alt+B | 将光标向后移动一个单词 | 单词导航 |
| Alt+F | 将光标向前移动一个单词 | 单词导航 |

### 主题和显示

| 快捷键 | 描述 | 上下文 |
|--------|------|--------|
| Ctrl+T | 切换代码块的语法突出显示 | /theme 选择器菜单内 |

### 多行输入

| 方法 | 快捷键 | 上下文 |
|------|--------|--------|
| 快速转义 | \ + Enter | 所有终端中工作 |
| macOS 默认 | Option+Enter | macOS 上的默认设置 |
| Shift+Enter | Shift+Enter | iTerm2、WezTerm、Ghostty、Kitty |
| 控制序列 | Ctrl+J | 多行的换行符 |
| 粘贴模式 | 直接粘贴 | 代码块、日志 |

### 快速命令

| 快捷键 | 描述 | 注释 |
|--------|------|------|
| / 在开始 | 命令或 skill | 请参阅内置命令和 skills |
| ! 在开始 | Bash 模式 | 直接运行命令 |
| @ | 文件路径提及 | 触发文件路径自动完成 |

---

## 内置命令

内置命令是常见操作的快捷方式。

| 命令 | 目的 |
|------|------|
| /clear | 清除对话历史 |
| /compact [instructions] | 压缩对话，可选的焦点说明 |
| /config | 打开设置界面（配置选项卡） |
| /context | 将当前上下文使用情况可视化为彩色网格 |
| /cost | 显示令牌使用统计 |
| /debug [description] | 排查当前会话的故障 |
| /doctor | 检查 Claude Code 安装的健康状况 |
| /exit | 退出 REPL |
| /export [filename] | 将当前对话导出到文件或剪贴板 |
| /help | 获取使用帮助 |
| /init | 使用 CLAUDE.md 指南初始化项目 |
| /mcp | 管理 MCP server 连接和 OAuth 身份验证 |
| /memory | 编辑 CLAUDE.md 内存文件 |
| /model | 选择或更改 AI 模型 |
| /permissions | 查看或更新权限 |
| /plan | 直接从提示进入 plan 模式 |
| /rename [name] | 重命名当前会话 |
| /resume [session] | 恢复对话 |
| /rewind | 回退对话和/或代码 |
| /stats | 可视化每日使用情况、会话历史 |
| /status | 打开设置界面（状态选项卡） |
| /statusline | 设置状态行 UI |
| /copy | 将最后一个响应复制到剪贴板 |
| /tasks | 列出和管理后台任务 |
| /teleport | 从 claude.ai 恢复远程会话 |
| /desktop | 移交给 Claude Code 桌面应用 |
| /theme | 更改颜色主题 |
| /todos | 列出当前 TODO 项 |
| /usage | 显示计划使用限制和速率限制状态 |

---

## Vim 编辑器模式

使用 `/vim` 命令启用 vim 风格编辑，或通过 `/config` 永久配置。

### 模式切换

| 命令 | 操作 | 来自模式 |
|------|------|----------|
| Esc | 进入 NORMAL 模式 | INSERT |
| i | 在光标前插入 | NORMAL |
| I | 在行首插入 | NORMAL |
| a | 在光标后插入 | NORMAL |
| A | 在行尾插入 | NORMAL |
| o | 在下方打开行 | NORMAL |
| O | 在上方打开行 | NORMAL |

### 导航（NORMAL 模式）

| 命令 | 操作 |
|------|------|
| h/j/k/l | 向左/下/上/右移动 |
| w | 下一个单词 |
| e | 单词末尾 |
| b | 上一个单词 |
| 0 | 行首 |
| $ | 行尾 |
| ^ | 第一个非空白字符 |
| gg | 输入开始 |
| G | 输入结束 |
| f{char} | 跳转到下一个字符出现 |
| F{char} | 跳转到上一个字符出现 |
| t{char} | 跳转到下一个字符出现之前 |
| T{char} | 跳转到上一个字符出现之后 |
| ; | 重复最后一个 f/F/t/T 动作 |
| , | 反向重复最后一个 f/F/t/T 动作 |

### 编辑（NORMAL 模式）

| 命令 | 操作 |
|------|------|
| x | 删除字符 |
| dd | 删除行 |
| D | 删除到行尾 |
| dw/de/db | 删除单词/到末尾/向后 |
| cc | 更改行 |
| C | 更改到行尾 |
| cw/ce/cb | 更改单词/到末尾/向后 |
| yy/Y | 复制行 |
| yw/ye/yb | 复制单词/到末尾/向后 |
| p | 在光标后粘贴 |
| P | 在光标前粘贴 |
| >> | 缩进行 |
| << | 取消缩进行 |
| J | 连接行 |
| . | 重复最后一个更改 |

### 文本对象（NORMAL 模式）

| 命令 | 操作 |
|------|------|
| iw/aw | 内部/周围单词 |
| iW/aW | 内部/周围 WORD |
| i"/a" | 内部/周围双引号 |
| i'/a' | 内部/周围单引号 |
| i(/a( | 内部/周围括号 |
| i[/a[ | 内部/周围方括号 |
| i{/a{ | 内部/周围大括号 |

---

## 命令历史

Claude Code 为当前会话维护命令历史：

- 输入历史按工作目录存储
- 运行 `/clear` 会重置输入历史
- 使用上/下箭头导航
- **注意**: 历史扩展（!）默认禁用

### 使用 Ctrl+R 反向搜索

1. 按 Ctrl+R 激活反向历史搜索
2. 输入文本以在以前的命令中搜索
3. 再次按 Ctrl+R 循环浏览较旧的匹配
4. 按 Tab 或 Esc 接受当前匹配并继续编辑
5. 按 Enter 接受并立即执行命令
6. 按 Ctrl+C 取消并恢复原始输入

---

## 后台 bash 命令

Claude Code 支持在后台运行 bash 命令。

### 后台运行的工作原理

- Claude Code 异步运行命令并立即返回后台任务 ID
- Claude Code 可以在命令继续在后台执行时响应新提示
- 输出被缓冲，Claude 可以使用 TaskOutput 工具检索它
- 后台任务有唯一的 ID 用于跟踪和输出检索

### 启用后台运行

- 提示 Claude Code 在后台运行命令
- 按 Ctrl+B 将常规 Bash 工具调用移到后台

### 常见的后台命令

- 构建工具（webpack、vite、make）
- 包管理器（npm、yarn、pnpm）
- 测试运行器（jest、pytest）
- 开发服务器
- 长时间运行的进程（docker、terraform）

---

## 使用 ! 前缀的 Bash 模式

通过在输入前加上 `!` 直接运行 bash 命令，无需通过 Claude：

```bash
! npm test
! git status
! ls -la
```

### Bash 模式特点

- 将命令及其输出添加到对话上下文
- 显示实时进度和输出
- 支持相同的 Ctrl+B 后台运行
- 不需要 Claude 解释或批准命令
- 支持基于历史的自动完成

---

## 提示建议

当您首次打开会话时，灰显的示例命令会出现在提示输入中。

- Claude Code 从您项目的 git 历史中选择命令
- Claude 响应后，建议继续根据对话历史出现
- 按 Tab 接受建议，或按 Enter 接受并提交
- 建议作为后台请求运行，额外成本最少

### 禁用提示建议

```bash
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

或在 `/config` 中切换设置。

---

## 任务列表

在处理复杂的多步工作时，Claude 会创建任务列表来跟踪进度。

- 任务出现在终端的状态区域中
- 按 Ctrl+T 切换任务列表视图
- 显示一次最多 10 个任务
- 任务在上下文压缩中持续存在

### 会话间共享任务列表

设置 `CLAUDE_CODE_TASK_LIST_ID` 以使用 `~/.claude/tasks/` 中的命名目录：

```bash
CLAUDE_CODE_TASK_LIST_ID=my-project claude
```

---

## PR 审查状态

在处理具有开放拉取请求的分支时，Claude Code 在页脚中显示可点击的 PR 链接。

### 状态颜色

- **绿色**: 已批准
- **黄色**: 待审查
- **红色**: 请求更改
- **灰色**: 草稿
- **紫色**: 已合并

### 使用方法

- Cmd+click（Mac）或 Ctrl+click（Windows/Linux）链接以在浏览器中打开
- 状态每 60 秒自动更新
- PR 状态需要安装并验证 gh CLI

---

## 相关链接

- [Skills](https://code.claude.com/docs/zh-CN/skills) - 自定义提示和工作流
- [Checkpointing](https://code.claude.com/docs/zh-CN/checkpointing) - 回退 Claude 的编辑
- [CLI reference](https://code.claude.com/docs/zh-CN/cli-reference) - 命令行标志和选项
- [Settings](https://code.claude.com/docs/zh-CN/settings) - 配置选项
- [Memory management](https://code.claude.com/docs/zh-CN/memory) - 管理 CLAUDE.md 文件
