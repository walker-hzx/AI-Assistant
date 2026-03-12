---
name: browser-debugger
description: "浏览器调试 - 捕获 Console 错误、网络请求失败、页面异常，DOM 样式检查。使用 Playwright 监听控制台和网络事件，获取元素 computed styles 排查样式问题"
model: sonnet
user-invocable: true
---

# 浏览器调试

自动捕获浏览器 Console 错误、网络请求失败、页面异常，以及 DOM 样式检查。

## 核心功能

| 功能 | 说明 |
|------|------|
| **Console 捕获** | 监听 console.log/error/warn 等 |
| **网络请求** | 捕获失败的 API 请求 |
| **页面异常** | 捕获 JavaScript 错误 |
| **截图功能** | 错误发生时自动截图 |
| **HAR 导出** | 导出完整网络请求记录 |
| **DOM 样式检查** | 获取元素的 computed styles、CSS 变量，选择器特异性分析 |

## 使用方式

### 1. 错误捕获（browser-capture.py）

```bash
# 捕获单个页面的错误
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/browser-capture.py https://example.com

# 捕获并导出 HAR
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/browser-capture.py https://example.com --har output.har

# 截图保存
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/browser-capture.py https://example.com --screenshot error.png
```

### 2. DOM 样式检查（dom-inspector.py）

```bash
# 获取元素的 computed styles
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector ".button" --styles

# 获取 CSS 变量（包括继承的）
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector "#header" --css-vars

# 获取元素完整信息
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector ".card" --info

# 分析选择器特异性（哪些规则匹配该元素）
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector ".btn-primary" --specificity

# 获取所有信息 + 截图
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector ".modal" --all --screenshot modal-debug.png
```

### 2. Skill 调用

在需要调试浏览器错误时，coordinator 会自动调度此 skill。

## 脚本参数

### browser-capture.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 要访问的 URL | - |
| `--wait` | 等待秒数 | 5 |
| `--har` | 导出 HAR 文件 | - |
| `--screenshot` | 错误时截图 | - |
| `--console-only` | 只捕获 console | false |

### dom-inspector.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `url` | 要访问的 URL | - |
| `--selector` / `-s` | CSS 选择器 | - |
| `--styles` / `-st` | 获取 computed styles | false |
| `--css-vars` / `-cv` | 获取 CSS 变量 | false |
| `--info` / `-i` | 获取元素基本信息 | false |
| `--specificity` / `-sp` | 分析选择器特异性 | false |
| `--all` / `-a` | 获取所有信息 | false |
| `--screenshot` / `-sh` | 截图输出路径 | - |
| `--output` / `-o` | JSON 输出文件 | - |
| `--wait` / `-w` | 等待秒数 | 3 |

## 输出格式

### Console 错误

```json
{
  "type": "console",
  "level": "error",
  "message": "Failed to load resource: net::ERR_CONNECTION_REFUSED",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 网络请求失败

```json
{
  "type": "network",
  "method": "GET",
  "url": "https://api.example.com/users",
  "status": 500,
  "response": "Internal Server Error",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 页面异常

```json
{
  "type": "page-error",
  "message": "Uncaught TypeError: Cannot read property 'foo' of undefined",
  "stack": "at Object.<anonymous> (/app.js:10:5)",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### DOM 样式检查输出

```json
{
  "url": "http://localhost:5173",
  "selector": ".button-primary",
  "data": {
    "computed_styles": {
      "display": "inline-flex",
      "position": "relative",
      "width": "120px",
      "height": "40px",
      "background": "rgb(59, 130, 246)",
      "color": "rgb(255, 255, 255)",
      "box-model": { ... }
    },
    "css_variables": {
      "--primary-color": "rgb(59, 130, 246)",
      "--btn-padding": "8px 16px"
    },
    "element_info": {
      "tag": "button",
      "id": null,
      "classes": ["btn", "btn-primary", "large"],
      "parent": "div",
      "bounds": { "x": 100, "y": 200, "width": 120, "height": 40 }
    }
  }
}
```

## 使用场景

### 场景 1：API 报错

```
用户：登录接口报错了，帮我看看

执行：
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/browser-capture.py http://localhost:3000/api/login

产出：
[ERROR] GET /api/login - 401 Unauthorized
[CONSOLE] Error: Invalid credentials
```

### 场景 2：页面加载失败

```
用户：首页加载不出来

执行：
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/browser-capture.py http://localhost:3000 --screenshot error.png

产出：
[PAGE-ERROR] Failed to load script bundle.js
[Screenshot] saved to error.png
```

### 场景 3：调试用户流程

```
用户：提交表单后有错误

执行：
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/browser-capture.py http://localhost:3000/form --har form-debug.har

产出：
[NETWORK] POST /api/submit - 422 Validation Error
[CONSOLE] ValidationError: email is required
```

### 场景 4：样式不生效

```
用户：按钮的 background-color 样式不生效

执行：
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector ".btn-primary" --styles --css-vars

产出：
{
  "computed_styles": {
    "background": "rgb(59, 130, 246)",
    "background-color": "rgb(59, 130, 246)"
  },
  "css_variables": {
    "--btn-bg": "rgb(59, 130, 246)"
  }
}
→ 分析：样式实际生效了，可能是视觉上不明显
```

### 场景 5：排查 CSS 变量未传递

```
用户：组件里的 CSS 变量获取不到

执行：
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector ".my-component" --css-vars

产出：
{
  "css_variables": {
    "--primary-color": "rgb(59, 130, 246)",
    "--component-bg": "rgba(0, 0, 0, 0.1) (继承, 父级 level 2)"
  }
}
→ 分析：变量来自父级的继承，需要检查定义位置
```

### 场景 6：选择器特异性冲突

```
用户：两个选择器都作用于同一元素，不知道哪个生效

执行：
python3 ~/.claude/plugins/marketplaces/ai-assistant/scripts/web/dom-inspector.py http://localhost:5173 --selector ".btn.primary" --specificity

产出：
{
  "selector_specificity": {
    "matchingRulesCount": 5,
    "topMatchingRules": [
      { "selector": ".btn.primary", "cssText": "..." },
      { "selector": ".btn", "cssText": "..." }
    ]
  }
}
→ 分析：.btn.primary 的特异性更高（0,2,0）
```

## 与 debugger 的关系

| 工具 | 职责 |
|------|------|
| **browser-debugger** | 捕获浏览器错误信息 + DOM 样式检查 |
| **debugger** | 分析错误原因，定位代码 Bug |

**工作流**：
1. browser-debugger 捕获错误 / DOM 样式
2. 将错误信息交给 debugger
3. debugger 分析并修复代码

**何时用 DOM 样式检查**：
- 样式不生效 → 获取 computed styles 确认实际生效的样式
- CSS 变量问题 → 获取变量值确认是否正确传递
- 选择器冲突 → 分析特异性确认哪个规则生效
- 布局问题 → 获取盒模型信息（margin/padding/border/width/height）

## 检查清单

### 错误捕获
- [ ] 确认 URL 可访问
- [ ] 成功捕获 Console 错误
- [ ] 成功捕获网络请求失败
- [ ] 成功捕获页面异常
- [ ] 提供了完整的错误信息
- [ ] 如需要，提供了截图或 HAR

### DOM 样式检查
- [ ] 确认选择器能匹配到元素
- [ ] 获取了 computed styles
- [ ] 排查了 CSS 变量问题（如需要）
- [ ] 分析了选择器特异性（如需要）
- [ ] 提供了截图（如需要）
- [ ] 基于样式分析给出了问题原因
